"""Check local profile links and SVG accessibility without network dependencies.

Checks README.md, Markdown under docs/, and SVG files under assets/. Markdown
links may be inline or use explicit reference syntax. Fenced/inline code is
ignored. External HTTP(S) and mailto links are not fetched or verified.
"""

from __future__ import annotations

import argparse
from html import unescape
from html.parser import HTMLParser
import math
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


INLINE_LINK = re.compile(
    r"(?P<image>!)?\[(?P<label>[^\]\n]*)\]\(\s*"
    r"(?P<url><[^>\n]+>|(?:[^\s()]|\([^()]*\))+)"
    r"(?:\s+[\"'][^\n]*?[\"'])?\s*\)"
)
REFERENCE = re.compile(r"^\s*\[([^\]\n]+)\]:\s*(<[^>\n]+>|\S+)", re.MULTILINE)
REFERENCE_LINK = re.compile(r"(!)?\[([^\]\n]*)\]\[([^\]\n]*)\]")


def prose_only(text: str, *, mask_inline: bool = True) -> str:
    """Mask code while retaining line numbers for diagnostics."""
    lines = []
    fence_char = ""
    fence_length = 0
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence_char:
            lines.append("\n" if line.endswith("\n") else "")
            if match and match[1][0] == fence_char and len(match[1]) >= fence_length:
                if not line[match.end():].strip():
                    fence_char = ""
            continue
        if match:
            fence_char, fence_length = match[1][0], len(match[1])
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(line)
    prose = "".join(lines)
    return re.sub(r"(`+)([^`\n]|(?!\1)`)*?\1", "", prose) if mask_inline else prose


class HtmlReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, int]] = []
        self.images: list[tuple[str | None, int]] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        line = self.getpos()[0]
        for key in (("id", "name") if tag == "a" else ("id",)):
            if values.get(key):
                self.anchors.add(values[key])
        if tag == "a" and values.get("href"):
            self.links.append((values["href"], line))
        if tag == "img":
            self.images.append((values.get("alt"), line))
            self.links.append((values.get("src") or "", line))


def markdown_anchors(text: str) -> set[str]:
    """Resolve conventional GitHub ATX/setext headings and explicit HTML IDs."""
    prose = prose_only(text, mask_inline=False)
    html = HtmlReferences()
    html.feed(prose)
    anchors = set(html.anchors)
    occurrences: dict[str, int] = {}
    lines = prose.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            heading = match[1]
        elif index + 1 < len(lines) and line.strip() and re.fullmatch(
            r"\s{0,3}(?:=+|-+)\s*", lines[index + 1]
        ):
            heading = line
        else:
            continue
        heading = INLINE_LINK.sub(lambda item: item["label"], heading)
        heading = unescape(re.sub(r"<[^>]+>", "", heading)).lower()
        slug = "".join(char for char in heading if char.isalnum() or char in " _-")
        slug = slug.replace(" ", "-")
        suffix = occurrences.get(slug, 0)
        occurrences[slug] = suffix + 1
        anchors.add(f"{slug}-{suffix}" if suffix else slug)
    return anchors


def check_link(root: Path, source: Path, target: str) -> str | None:
    target = unescape(target.strip().removeprefix("<").removesuffix(">"))
    if not target:
        return "empty link or image source"
    try:
        parsed = urlsplit(target)
    except ValueError:
        return f"invalid link: {target}"
    if parsed.scheme in {"https", "http", "mailto"} or parsed.netloc:
        return None
    if parsed.scheme:
        return f"unsupported link scheme: {parsed.scheme}"
    relative = unquote(parsed.path).replace("\\", "/")
    destination = (
        root / relative.lstrip("/") if relative.startswith("/") else source.parent / relative
    ) if relative else source
    destination = destination.resolve()
    if not destination.is_relative_to(root.resolve()):
        return f"local link escapes repository: {target}"
    if not destination.exists():
        return f"missing local target: {target}"
    if parsed.fragment and destination.is_file() and destination.suffix.lower() == ".md":
        if unquote(parsed.fragment) not in markdown_anchors(destination.read_text(encoding="utf-8")):
            return f"missing heading or anchor: {target}"
    return None


def check_markdown(root: Path, path: Path) -> list[str]:
    text = prose_only(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    links: list[tuple[str, int]] = []

    def report(line: int, reason: str) -> None:
        errors.append(f"{path.relative_to(root).as_posix()}:{line}: {reason}")

    for match in INLINE_LINK.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        links.append((match["url"], line))
        if match["image"] and not match["label"].strip():
            report(line, "image needs descriptive alt text")
    references = {" ".join(match[1].lower().split()): match[2] for match in REFERENCE.finditer(text)}
    for match in REFERENCE_LINK.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        reference = " ".join((match[3] or match[2]).lower().split())
        if reference not in references:
            report(line, f"undefined link reference: {reference}")
        else:
            links.append((references[reference], line))
        if match[1] and not match[2].strip():
            report(line, "image needs descriptive alt text")
    html = HtmlReferences()
    html.feed(text)
    links.extend(html.links)
    for alt, line in html.images:
        if not alt or not alt.strip():
            report(line, "image needs descriptive alt text")
    for target, line in links:
        if reason := check_link(root, path, target):
            report(line, reason)
    return errors


def check_svg(root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    name = path.relative_to(root).as_posix()
    try:
        svg = ET.fromstring(path.read_text(encoding="utf-8"))
    except ET.ParseError as error:
        return [f"{name}: malformed SVG: {error}"]
    def local_name(value: str) -> str:
        return value.rsplit("}", 1)[-1]

    if local_name(svg.tag) != "svg":
        errors.append(f"{name}: root element must be svg")
    try:
        box = [float(value) for value in re.split(r"[\s,]+", svg.attrib.get("viewBox", "").strip())]
        valid_box = len(box) == 4 and all(math.isfinite(value) for value in box) and box[2] > 0 and box[3] > 0
    except ValueError:
        valid_box = False
    if not valid_box:
        errors.append(f"{name}: needs a finite viewBox with positive width and height")
    for element_name in ("title", "desc"):
        if not any(local_name(child.tag) == element_name and "".join(child.itertext()).strip() for child in svg):
            errors.append(f"{name}: needs a nonempty {element_name} for accessibility")
    for element in svg.iter():
        tag = local_name(element.tag).lower()
        if tag in {"script", "foreignobject"}:
            errors.append(f"{name}: unsafe SVG element: {tag}")
        for key, value in element.attrib.items():
            attribute = local_name(key).lower()
            if attribute.startswith("on"):
                errors.append(f"{name}: SVG event handlers are forbidden: {attribute}")
            if attribute in {"href", "src"} and value and not value.startswith("#"):
                errors.append(f"{name}: SVG resources must use local fragment references")
        css = " ".join(element.attrib.values()) + " " + (element.text or "")
        if re.search(r"@import", css, re.IGNORECASE):
            errors.append(f"{name}: SVG CSS imports are forbidden")
        for url in re.findall(r"url\(\s*([^)]*)\)", css, re.IGNORECASE):
            if not url.strip(" \t\r\n\"'").startswith("#"):
                errors.append(f"{name}: SVG CSS must not load external resources")
    return errors


def check_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    readme = root / "README.md"
    if not readme.is_file():
        errors.append("README.md: missing profile README")
    markdown = ([readme] if readme.is_file() else []) + sorted((root / "docs").rglob("*.md"))
    for path in markdown:
        errors.extend(check_markdown(root, path))
    for path in sorted((root / "assets").rglob("*.svg")):
        errors.extend(check_svg(root, path))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check_repository(args.root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"Profile checks failed: {len(errors)} issue(s).", file=sys.stderr)
        return 1
    print("Profile checks passed (local links, image alt text, and SVG assets).")
    print("External links were not fetched; review their destinations separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
