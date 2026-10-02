# Maintaining this profile

This repository is the source for the profile README. Keep the front page short
enough to scan, and put implementation details in the linked project write-ups.
All validation tools use the Python standard library.

## Where to edit

| Change | File |
|---|---|
| Introduction, navigation, contact, and featured work | [README.md](../README.md) |
| Structured project metadata | [projects.json](../projects.json) |
| Generated project index | [project-index.md](project-index.md) |
| Project evidence and current scope | Files in `docs/projects/` |
| Light/dark header artwork | `assets/profile-light.svg` and `assets/profile-dark.svg` |

## Add a project

1. Check the current repository contents and choose an accurate scope label.
2. Add a write-up with the problem, implemented behavior, source links, and limits.
3. Add a unique entry to `projects.json`, including its local write-up path.
4. Regenerate the index and run the checks below.
5. Feature it on the front page only if it adds useful evidence for a visitor.

Empty repositories and planned features should not be presented as completed
applications. Keep reported test results tied to the run or PR that recorded them.
Use commit-specific source links when discussing a particular implementation.

## Check an edit

Run from this repository's root with Python 3.11 or newer:

```sh
python -B scripts/render_catalog.py
python -B scripts/render_catalog.py --check
python -B scripts/check_profile.py
python -B -m unittest discover -s tests -v
```

The catalog check detects stale generated output. The profile checker checks local
links, heading anchors, image alternative text, and SVG safety. The unit tests
exercise failure cases. GitHub Actions runs these checks on pushes and pull requests.

External destinations are not fetched by the checker; review them separately.
Preview the README in GitHub's rendered view and inspect both banner themes when
changing artwork. Keep artwork text readable and avoid relying on color alone.

## Keep changes reviewable

Use UTF-8 and LF line endings. Keep a commit focused on one meaningful improvement,
explain its purpose, and include the checks relevant to that change. Never include
tokens, credentials, private data, or unverified performance claims in profile files.

[Back to profile](../README.md)
