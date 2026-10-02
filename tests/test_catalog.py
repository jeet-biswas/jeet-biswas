"""Regression tests for project metadata, safe rendering, and stale-output detection."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import render_catalog as catalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "docs/projects").mkdir(parents=True)
        (self.root / "docs/projects/demo.md").write_text("# Demo\n", encoding="utf-8")
        self.project = {
            "id": "demo", "name": "Demo", "repository": "https://github.com/jeet-biswas/demo",
            "focus": "A small example", "status": "Prototype", "case_study": "docs/projects/demo.md",
        }

    def write(self, value):
        (self.root / "projects.json").write_text(json.dumps(value), encoding="utf-8")

    def valid(self):
        self.write({"schema_version": 1, "projects": [self.project]})

    def test_real_catalog_round_trip(self):
        projects = catalog.load_projects(catalog.ROOT)
        self.assertGreaterEqual(len(projects), 1)
        self.assertEqual((catalog.ROOT / catalog.OUTPUT).read_text(encoding="utf-8"),
                         catalog.render_catalog(projects))

    def test_duplicate_ids_are_rejected(self):
        self.write({"schema_version": 1, "projects": [self.project, self.project]})
        with self.assertRaisesRegex(ValueError, "duplicate"):
            catalog.load_projects(self.root)

    def test_rejects_external_or_injected_repository_urls(self):
        for url in ("http://github.com/a/b", "https://github.com.evil.test/a/b",
                    "https://name@github.com/a/b", "javascript:alert(1)",
                    "https://github.com/a/b?redirect=elsewhere"):
            with self.subTest(url=url):
                self.project["repository"] = url
                self.valid()
                with self.assertRaisesRegex(ValueError, "canonical"):
                    catalog.load_projects(self.root)

    def test_case_study_cannot_escape_docs_or_be_missing(self):
        for path in ("../outside.md", "docs/../../outside.md", "docs/missing.md", "/tmp/demo.md"):
            with self.subTest(path=path):
                self.project["case_study"] = path
                self.valid()
                with self.assertRaises(ValueError):
                    catalog.load_projects(self.root)

    def test_invalid_top_level_and_missing_fields(self):
        for value in ([], {}, {"schema_version": 2, "projects": []},
                      {"schema_version": 1, "projects": [{}]}):
            with self.subTest(value=value):
                self.write(value)
                with self.assertRaises(ValueError):
                    catalog.load_projects(self.root)

    def test_renderer_escapes_table_and_html_content(self):
        self.project["focus"] = "<script>alert(1)</script> | [fake](url)\nsecond line"
        rendered = catalog.render_catalog([self.project])
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("\\|", rendered)
        self.assertIn("\\[fake\\]", rendered)
        self.assertNotIn("\nsecond line", rendered)

    def test_cli_check_detects_missing_and_stale_output(self):
        self.valid()
        with patch.object(catalog, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            with patch("sys.argv", ["render_catalog.py", "--check"]):
                self.assertEqual(catalog.main(), 1)
            with patch("sys.argv", ["render_catalog.py"]):
                self.assertEqual(catalog.main(), 0)
            with patch("sys.argv", ["render_catalog.py", "--check"]):
                self.assertEqual(catalog.main(), 0)
                (self.root / catalog.OUTPUT).write_text("stale", encoding="utf-8")
                self.assertEqual(catalog.main(), 1)


if __name__ == "__main__":
    unittest.main()
