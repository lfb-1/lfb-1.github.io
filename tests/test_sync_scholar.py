import importlib.util
import sys
from dataclasses import replace
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from argparse import Namespace
import os
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_scholar.py"
SPEC = importlib.util.spec_from_file_location("sync_scholar", MODULE_PATH)
assert SPEC and SPEC.loader
sync_scholar = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_scholar
SPEC.loader.exec_module(sync_scholar)


SAMPLE_HTML = """
<html><body><table>
<tr class="gsc_a_tr">
  <td class="gsc_a_t">
    <a href="/citations?view_op=view_citation&amp;hl=en&amp;user=test&amp;citation_for_view=test:abc123" class="gsc_a_at">A Paper &amp; Its Result</a>
    <div class="gs_gray">F Liu, A Author</div>
    <div class="gs_gray">CVPR 2026<span class="gs_oph">, 2025</span></div>
  </td>
  <td class="gsc_a_c"><a class="gsc_a_ac gs_ibl">12</a></td>
  <td class="gsc_a_y"><span class="gsc_a_h gsc_a_hc gs_ibl">2026</span></td>
</tr>
<tr class="gsc_a_tr">
  <td class="gsc_a_t">
    <a href="/citations?view_op=view_citation&amp;citation_for_view=test:def456" class="gsc_a_at">Second Paper</a>
    <div class="gs_gray">B Author, F Liu</div>
    <div class="gs_gray">Journal Name</div>
  </td>
  <td class="gsc_a_c"><a class="gsc_a_ac gs_ibl"></a></td>
  <td class="gsc_a_y"><span class="gsc_a_h gsc_a_hc gs_ibl">2025</span></td>
</tr>
</table></body></html>
"""


def valid_record(index: int, *, profile: str = sync_scholar.SCHOLAR_USER):
    return sync_scholar.Publication(
        scholar_id=f"record-{index}",
        title=f"Publication {index}",
        authors="F Liu, A Author",
        venue="Journal",
        year=2026,
        citations=index,
        url=(
            "https://scholar.google.com/citations?view_op=view_citation"
            f"&citation_for_view={profile}:record-{index}"
        ),
    )


class ScholarParserTests(unittest.TestCase):
    def test_parse_profile_extracts_rows_and_ignores_hidden_venue_suffix(self):
        records = sync_scholar.parse_profile(SAMPLE_HTML)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].scholar_id, "abc123")
        self.assertEqual(records[0].title, "A Paper & Its Result")
        self.assertEqual(records[0].authors, "F Liu, A Author")
        self.assertEqual(records[0].venue, "CVPR 2026")
        self.assertEqual(records[0].year, 2026)
        self.assertEqual(records[0].citations, 12)
        self.assertTrue(records[0].url.startswith("https://scholar.google.com/citations?"))
        self.assertEqual(records[1].citations, 0)

    def test_recent_sort_prefers_first_author_within_year(self):
        records = sync_scholar.parse_profile(SAMPLE_HTML)
        coauthor = sync_scholar.Publication(
            scholar_id="coauthor",
            title="Highly cited coauthor paper",
            authors="A Author, F Liu",
            venue="CVPR 2026",
            year=2026,
            citations=999,
            url="https://example.test/coauthor",
        )

        ordered = sorted(records + [coauthor], key=sync_scholar.publication_sort_key)

        self.assertEqual(ordered[0].scholar_id, "abc123")
        self.assertEqual(ordered[1].scholar_id, "coauthor")

    def test_format_venue_expands_journal_alias_and_preserves_details(self):
        self.assertEqual(
            sync_scholar.format_venue("IEEE TPAMI 48 (1), 1-10"),
            (
                "IEEE Transactions on Pattern Analysis and Machine Intelligence "
                "(TPAMI) 48 (1), 1-10"
            ),
        )
        self.assertEqual(
            sync_scholar.format_venue("IEEE Transactions on Image Processing"),
            "IEEE Transactions on Image Processing (TIP)",
        )
        self.assertEqual(
            sync_scholar.format_venue("CVPR 2026"),
            "CVPR 2026",
        )
        self.assertEqual(
            sync_scholar.format_venue(
                "European Heart Journal-Digital Health 7 (6), ztag064"
            ),
            "European Heart Journal - Digital Health (EHJ-DH) 7 (6), ztag064",
        )

    def test_update_homepage_replaces_only_marked_block(self):
        records = sync_scholar.parse_profile(SAMPLE_HTML)
        initial = "before\n<!-- PUBLICATIONS_AUTO:START -->\nold\n<!-- PUBLICATIONS_AUTO:END -->\nafter\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.html"
            path.write_text(initial, encoding="utf-8")

            sync_scholar.update_homepage(path, records)
            updated = path.read_text(encoding="utf-8")

        self.assertIn("A Paper &amp; Its Result", updated)
        self.assertIn("CVPR 2026", updated)
        self.assertNotIn("\nold\n", updated)
        self.assertTrue(updated.startswith("before\n"))
        self.assertTrue(updated.endswith("\nafter\n"))

    def test_update_homepage_uses_full_cv_authors(self):
        records = sync_scholar.parse_profile(SAMPLE_HTML)
        cv_records = [
            {
                "title": "A Paper & Its Result",
                "authors": "Fengbei Liu, Alice Author",
                "venue": "CVPR",
                "year": "2026",
            }
        ]
        initial = "<!-- PUBLICATIONS_AUTO:START -->\nold\n<!-- PUBLICATIONS_AUTO:END -->"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.html"
            path.write_text(initial, encoding="utf-8")
            sync_scholar.update_homepage(path, records, cv_records)
            updated = path.read_text(encoding="utf-8")

        self.assertIn("Fengbei Liu, Alice Author", updated)
        self.assertNotIn(">F Liu, A Author</span>", updated)

    def test_update_homepage_prefers_cv_acceptance_over_preprint_venue(self):
        publication = sync_scholar.Publication(
            scholar_id="madam",
            title="MAdam: Metric-Aware Multi-Objective Adam",
            authors="F Liu, A Author",
            venue="arXiv preprint arXiv:2606.03904",
            year=2026,
            citations=1,
            url="https://example.test/madam",
        )
        cv_records = [
            {
                "title": publication.title,
                "authors": "Fengbei Liu, Alice Author",
                "venue": "NeurIPS",
                "year": "2026",
                "entry_type": "publication",
            }
        ]
        initial = "<!-- PUBLICATIONS_AUTO:START -->\nold\n<!-- PUBLICATIONS_AUTO:END -->"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.html"
            path.write_text(initial, encoding="utf-8")
            sync_scholar.update_homepage(path, [publication], cv_records)
            updated = path.read_text(encoding="utf-8")

        self.assertIn("NeurIPS 2026", updated)
        self.assertNotIn("arXiv preprint", updated)

    def test_homepage_preserves_deliberate_title_exclusions(self):
        excluded = sync_scholar.Publication(
            scholar_id="excluded",
            title="An example: the CT–LVEF study",
            authors="F Liu",
            venue="Journal",
            year=2027,
            citations=100,
            url="https://example.test/excluded",
        )
        records = [excluded] + sync_scholar.parse_profile(SAMPLE_HTML)
        initial = "<!-- PUBLICATIONS_AUTO:START -->\nold\n<!-- PUBLICATIONS_AUTO:END -->"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.html"
            path.write_text(initial, encoding="utf-8")
            sync_scholar.update_homepage(path, records)
            updated = path.read_text(encoding="utf-8")

        self.assertNotIn("CT-LVEF", updated)
        self.assertIn("A Paper &amp; Its Result", updated)

    def test_validate_profile_rejects_partial_response(self):
        records = sync_scholar.parse_profile(SAMPLE_HTML)
        with self.assertRaisesRegex(RuntimeError, "Refusing to replace"):
            sync_scholar.validate_profile(records, previous_count=40)

    def test_validate_profile_rejects_wrong_profile(self):
        records = [valid_record(index, profile="another-user") for index in range(10)]
        with self.assertRaisesRegex(RuntimeError, "wrong profile"):
            sync_scholar.validate_profile(records, previous_count=0)

    def test_validate_profile_rejects_field_level_parse_failure(self):
        records = [valid_record(index) for index in range(10)]
        records[0] = replace(records[0], authors="")
        with self.assertRaisesRegex(RuntimeError, "metadata coverage"):
            sync_scholar.validate_profile(records, previous_count=0)

    def test_load_previous_count_rejects_corrupt_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scholar.json"
            path.write_text("not json", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "snapshot is unreadable"):
                sync_scholar.load_previous_count(path)

    def test_snapshot_order_is_independent_of_input_order(self):
        left = valid_record(1)
        right = replace(left, scholar_id="record-2", url=left.url.replace("record-1", "record-2"))
        payload_a = sync_scholar.snapshot_payload([left, right])
        payload_b = sync_scholar.snapshot_payload([right, left])
        self.assertEqual(payload_a, payload_b)


class InventoryMatchTests(unittest.TestCase):
    def test_cv_inventory_includes_publications_and_preprints(self):
        tex = r"""
        \resumePubheading{Published Work}{Fengbei Liu, A Author}{Journal 2024}
        \resumeArxivheading{Preprint Work}{Fengbei Liu, B Author}{arXiv:1234, 2025}
        """
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cv.tex"
            path.write_text(tex, encoding="utf-8")
            records = sync_scholar.load_cv_publications(path)

        self.assertEqual(len(records), 2)
        self.assertEqual(
            {record["entry_type"] for record in records},
            {"publication", "preprint"},
        )
        self.assertEqual(records[0]["authors"], "Fengbei Liu, A Author")
        self.assertEqual(records[1]["authors"], "Fengbei Liu, B Author")

    def test_fuzzy_title_match_accepts_minor_scholar_title_difference(self):
        scholar = [
            sync_scholar.Publication(
                scholar_id="rned",
                title="RNED: Rotary Number Encoding and Decoding for Medical VLMs",
                authors="F Liu",
                venue="CVPR 2026",
                year=2026,
                citations=0,
                url="https://example.test/rned",
            )
        ]
        cv = [
            {
                "title": "RNED: Rotary Number Encoding and Decoding for Quantitative Medical VLM Analysis",
                "venue": "CVPR",
                "year": "2026",
            }
        ]

        matches, scholar_only, cv_only = sync_scholar.match_inventory(scholar, cv)

        self.assertEqual(len(matches), 1)
        self.assertLess(matches[0][2], 1.0)
        self.assertEqual(scholar_only, [])
        self.assertEqual(cv_only, [])

    def test_sync_report_discloses_duplicate_and_fuzzy_matches(self):
        scholar = [
            sync_scholar.Publication(
                scholar_id="journal",
                title="RNED: Rotary Number Encoding and Decoding for Medical VLMs",
                authors="F Liu",
                venue="CVPR 2026",
                year=2026,
                citations=2,
                url="https://example.test/journal",
            ),
            sync_scholar.Publication(
                scholar_id="preprint",
                title="RNED: Rotary Number Encoding and Decoding for Medical VLMs",
                authors="F Liu",
                venue="arXiv preprint",
                year=2026,
                citations=1,
                url="https://example.test/preprint",
            ),
        ]
        cv = [
            {
                "title": "RNED: Rotary Number Encoding and Decoding for Quantitative Medical VLM Analysis",
                "venue": "CVPR",
                "year": "2026",
            }
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.md"
            sync_scholar.write_sync_report(path, scholar, cv)
            report = path.read_text(encoding="utf-8")

        self.assertIn("Fuzzy title matches requiring review: 1", report)
        self.assertIn("Scholar duplicate-version groups: 1", report)
        self.assertIn("similarity", report)
        self.assertIn("arXiv preprint", report)


class FetchRecoveryTests(unittest.TestCase):
    def test_access_denials_are_distinct_and_not_retried(self):
        for status in (403, 429):
            with self.subTest(status=status), patch.object(
                sync_scholar, "urlopen",
                side_effect=HTTPError(sync_scholar.PROFILE_URL, status, "denied", {}, None),
            ) as fetch:
                with self.assertRaisesRegex(sync_scholar.ScholarAccessBlocked, "No records were refreshed"):
                    sync_scholar.fetch_profile()
                self.assertEqual(fetch.call_count, 1)

    def test_unexpected_http_and_network_errors_still_fail(self):
        for error in (HTTPError(sync_scholar.PROFILE_URL, 500, "error", {}, None),
                      URLError("unreachable"), TimeoutError("timeout")):
            with self.subTest(error=error), patch.object(sync_scholar, "urlopen", side_effect=error):
                with self.assertRaises(RuntimeError) as caught:
                    sync_scholar.fetch_profile()
                self.assertNotIsInstance(caught.exception, sync_scholar.ScholarAccessBlocked)

    def test_blocked_cli_is_nonzero_and_reports_stale_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            summary = Path(directory) / "summary.md"
            with patch.object(sync_scholar, "fetch_profile", side_effect=sync_scholar.ScholarAccessBlocked("blocked")), \
                 patch.object(sync_scholar, "parse_args", return_value=Namespace(html=None, timeout=30)), \
                 patch.object(sync_scholar, "write_snapshot") as snapshot, \
                 patch.object(sync_scholar, "update_homepage") as homepage, \
                 patch.object(sync_scholar, "write_sync_report") as report, \
                 patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(summary)}):
                self.assertEqual(sync_scholar.cli(), 78)
                snapshot.assert_not_called()
                homepage.assert_not_called()
                report.assert_not_called()
            self.assertIn("data NOT refreshed", summary.read_text())

    def test_malformed_consent_and_partial_saved_html_preserve_files(self):
        for html in ("<html>Before you continue to Google</html>",
                     "<html>unusual traffic CAPTCHA</html>", "<tr broken", SAMPLE_HTML):
            with self.subTest(html=html), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "data").mkdir()
                saved = root / "input.html"
                saved.write_text(html)
                files = {root / "index.html": "original homepage", root / "data/scholar.json":
                         '{"publications": []}', root / "data/sync_report.md": "original report"}
                for path, content in files.items():
                    path.write_text(content)
                with patch.object(sync_scholar, "ROOT", root), \
                     patch.object(sync_scholar, "parse_args", return_value=Namespace(html=saved, timeout=30)), \
                     patch.object(sync_scholar, "urlopen") as network:
                    with self.assertRaises(RuntimeError):
                        sync_scholar.main()
                    network.assert_not_called()
                for path, content in files.items():
                    self.assertEqual(path.read_text(), content)

    def test_valid_saved_html_runs_offline_and_preserves_exclusions(self):
        rows = []
        for i in range(10):
            title = "The CT–LVEF study" if i == 0 else f"Publication {i}"
            rows.append(f'''<tr class="gsc_a_tr"><td><a class="gsc_a_at"
                href="/citations?citation_for_view={sync_scholar.SCHOLAR_USER}:id{i}">{title}</a>
                <div class="gs_gray">F Liu</div><div class="gs_gray">Journal</div></td>
                <td><span class="gsc_a_h">2026</span></td></tr>''')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            saved = root / "input.html"
            saved.write_text("<table>" + "".join(rows) + "</table>")
            (root / "index.html").write_text("before\n" + sync_scholar.START_MARKER +
                "\nold\n" + sync_scholar.END_MARKER + "\nafter")
            with patch.object(sync_scholar, "ROOT", root), \
                 patch.object(sync_scholar, "load_cv_publications", return_value=[]), \
                 patch.object(sync_scholar, "parse_args", return_value=Namespace(html=saved, timeout=30)), \
                 patch.object(sync_scholar, "urlopen") as network:
                self.assertEqual(sync_scholar.main(), 0)
                network.assert_not_called()
            homepage = (root / "index.html").read_text()
            self.assertNotIn("CT–LVEF", homepage)
            self.assertTrue(homepage.startswith("before\n"))
            self.assertTrue(homepage.endswith("\nafter"))
            self.assertEqual(sync_scholar.load_previous_count(root / "data/scholar.json"), 10)


if __name__ == "__main__":
    unittest.main()

