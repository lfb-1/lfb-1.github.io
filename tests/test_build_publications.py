import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SPEC = importlib.util.spec_from_file_location(
    "build_publications", SCRIPTS / "build_publications.py"
)
assert SPEC and SPEC.loader
build_publications = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
    SPEC.loader.exec_module(build_publications)


class PublicationInventoryTests(unittest.TestCase):
    def test_keeps_undated_papers_contributions_accents_and_preprints(self):
        tex = r"""
        \section{Publications}
        \resumePubheading{A Published Paper}
        {L\'eo Author$^*$, \textbf{Fengbei Liu}$^*$}{MICCAI 2026, Oral}
        \resumePubheading{Longitudinal ECGs}
        {Sunwoo Kwak, \textbf{Fengbei Liu}}{JACC: Advances}
        \resumeArxivheading{A Preprint}{Fengbei Liu}{arXiv:1234, 2025}
        """
        snapshot = {
            "publications": [
                {
                    "scholar_id": "published",
                    "title": "A Published Paper",
                    "authors": "L Author, F Liu",
                    "venue": "MICCAI 2026",
                    "year": 2026,
                    "citations": 0,
                    "url": "https://example.org/published",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cv = root / "cv.tex"
            scholar = root / "scholar.json"
            cv.write_text(tex)
            scholar.write_text(json.dumps(snapshot))
            payload = build_publications.build_inventory(cv, scholar)
            rows = payload["publications"]
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["authors"], "Léo Author*, Fengbei Liu*")
        self.assertEqual(rows[0]["qualifiers"], ["Oral"])
        self.assertEqual(rows[0]["url"], "https://example.org/published")
        self.assertEqual(rows[1]["venue"], "JACC: Advances")
        self.assertEqual(rows[1]["year"], "")
        self.assertEqual(rows[1]["url"], "")
        self.assertEqual(rows[2]["kind"], "preprint")
        self.assertEqual(rows[2]["venue"], "arXiv:1234")
        self.assertEqual(rows[2]["year"], "2025")

    def test_duplicate_cv_titles_are_rejected(self):
        paper = r"\resumePubheading{Same Paper}{Fengbei Liu}{CVPR 2026}"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cv = root / "cv.tex"
            scholar = root / "scholar.json"
            cv.write_text(paper + "\n" + paper)
            scholar.write_text('{"publications": []}')
            with self.assertRaisesRegex(
                RuntimeError, "Duplicate CV publication"
            ):
                build_publications.build_inventory(cv, scholar)


if __name__ == "__main__":
    unittest.main()
