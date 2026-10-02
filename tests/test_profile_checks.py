"""Regression cases for public profile links and self-contained SVG assets."""

from pathlib import Path
import tempfile
import unittest

from scripts.check_profile import check_repository


SAFE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 30">
<title>Profile banner</title><desc>A compact introduction to the portfolio.</desc>
<defs><linearGradient id="accent" /></defs>
<rect width="100" height="30" fill="url(#accent)" />
</svg>"""


class ProfileChecksTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write("README.md", "# Profile\n")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def errors(self):
        return "\n".join(check_repository(self.root))

    def test_valid_profile_with_relative_links_anchors_and_svg(self):
        self.write("README.md", """# Profile
![Profile banner](assets/banner.svg)
[Projects](docs/projects.md#selected-projects)
[Contact][contact]
[contact]: mailto:person@domain.test
<a href="https://github.com/person">GitHub</a>
""")
        self.write("docs/projects.md", "## Selected projects\n[Back](../README.md#profile)\n")
        self.write("assets/banner.svg", SAFE_SVG)
        self.assertEqual(check_repository(self.root), [])

    def test_missing_local_document_and_heading_are_reported(self):
        self.write("README.md", "# Profile\n[Missing](docs/missing.md)\n[Wrong](#missing)\n")
        errors = self.errors()
        self.assertIn("README.md:2: missing local target", errors)
        self.assertIn("README.md:3: missing heading or anchor", errors)

    def test_parent_path_and_encoded_traversal_cannot_escape_repository(self):
        for target in ("../outside.md", "%2e%2e/outside.md"):
            with self.subTest(target=target):
                self.write("README.md", f"[Outside]({target})\n")
                self.assertIn("escapes repository", self.errors())

    def test_code_samples_do_not_create_false_link_failures(self):
        self.write("README.md", """# Profile
`[example](missing.md)`
````markdown
[example](missing.md)
```
![example](missing.svg)
````
~~~html
<img src="missing.svg">
~~~
""")
        self.assertEqual(check_repository(self.root), [])

    def test_both_html_and_markdown_images_need_alt_text(self):
        self.write("assets/banner.svg", SAFE_SVG)
        self.write("README.md", '<img src="assets/banner.svg">\n![](assets/banner.svg)\n')
        self.assertEqual(self.errors().count("image needs descriptive alt text"), 2)

    def test_html_image_paths_and_anchors_are_checked(self):
        self.write("README.md", '<a id="contact"></a>\n[Contact](#contact)\n<img src="absent.svg" alt="Banner">\n')
        errors = self.errors()
        self.assertIn("missing local target: absent.svg", errors)
        self.assertNotIn("missing heading", errors)

    def test_duplicate_headings_get_distinct_anchors(self):
        self.write("README.md", "# Profile\n## Notes\n## Notes\n[Second](#notes-1)\n")
        self.assertEqual(check_repository(self.root), [])

    def test_heading_with_inline_code_keeps_its_anchor_text(self):
        self.write("README.md", "# Using `Python`\n[Language](#using-python)\n")
        self.assertEqual(check_repository(self.root), [])

    def test_reference_links_report_undefined_and_missing_destinations(self):
        self.write("README.md", "[Guide][guide]\n[Absent][absent]\n\n[guide]: docs/guide.md\n")
        errors = self.errors()
        self.assertIn("undefined link reference: absent", errors)
        self.assertIn("missing local target: docs/guide.md", errors)

    def test_unsafe_link_scheme_is_reported(self):
        self.write("README.md", '<a href="javascript:alert(1)">Unsafe</a>\n')
        self.assertIn("unsupported link scheme", self.errors())

    def test_svg_requires_accessible_metadata_and_valid_dimensions(self):
        self.write("assets/banner.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 0 10"/>')
        errors = self.errors()
        self.assertIn("positive width and height", errors)
        self.assertIn("nonempty title", errors)
        self.assertIn("nonempty desc", errors)

    def test_svg_rejects_scripts_event_handlers_and_remote_resources(self):
        cases = {
            '<script>alert(1)</script>': "unsafe SVG element",
            '<rect onclick="alert(1)"/>': "event handlers are forbidden",
            '<image href="https://host.test/banner.png"/>': "local fragment references",
            '<style>rect {fill: url(https://host.test/pattern.svg)}</style>': "must not load external resources",
            '<style>@import "https://host.test/style.css";</style>': "CSS imports are forbidden",
        }
        for snippet, expected in cases.items():
            with self.subTest(snippet=snippet):
                self.write("assets/banner.svg", SAFE_SVG.replace("</svg>", snippet + "</svg>"))
                self.assertIn(expected, self.errors())

    def test_malformed_svg_has_an_actionable_failure(self):
        self.write("assets/banner.svg", "<svg><broken></svg>")
        self.assertIn("assets/banner.svg: malformed SVG", self.errors())

    def test_root_relative_and_escaped_filename_links_work(self):
        self.write("docs/Project notes.md", "# Project notes\n")
        self.write("README.md", "[Notes](/docs/Project%20notes.md#project-notes)\n")
        self.assertEqual(check_repository(self.root), [])


if __name__ == "__main__":
    unittest.main()
