import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/publish_cv.py"
SPEC = importlib.util.spec_from_file_location("publish_cv", MODULE_PATH)
assert SPEC and SPEC.loader
publish_cv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publish_cv)


class PublishCVTests(unittest.TestCase):
    def test_public_pdf_and_all_links_use_the_compiled_cv(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cv").mkdir()
            pdf = b"%PDF-1.4\ncompiled CV\n"
            (root / "cv/fbl_cv.pdf").write_bytes(pdf)
            (root / "config.yml").write_text(
                "buttons: fbl_cv.pdf?v=123abc\n"
                "social: fbl_cv.pdf?v=abcdef\n"
                "news: keep curated news\n"
            )
            with patch.object(publish_cv, "ROOT", root):
                self.assertEqual(publish_cv.main(), 0)
            version = hashlib.sha256(pdf).hexdigest()[:8]
            self.assertEqual((root / "static/fbl_cv.pdf").read_bytes(), pdf)
            config = (root / "config.yml").read_text()
            self.assertEqual(config.count(f"fbl_cv.pdf?v={version}"), 2)
            self.assertIn("news: keep curated news", config)

    def test_missing_link_does_not_replace_the_public_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cv").mkdir()
            (root / "static").mkdir()
            (root / "cv/fbl_cv.pdf").write_bytes(b"%PDF-1.4\nnew")
            (root / "static/fbl_cv.pdf").write_bytes(b"%PDF-1.4\nold")
            (root / "config.yml").write_text("news: []\n")
            with patch.object(publish_cv, "ROOT", root):
                with self.assertRaisesRegex(
                    RuntimeError, "no versioned CV link"
                ):
                    publish_cv.main()
            self.assertEqual(
                (root / "static/fbl_cv.pdf").read_bytes(), b"%PDF-1.4\nold"
            )
            self.assertEqual((root / "config.yml").read_text(), "news: []\n")


if __name__ == "__main__":
    unittest.main()
