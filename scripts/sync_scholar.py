#!/usr/bin/env python3
"""Synchronize the public Google Scholar profile into this Pages repository.

Google Scholar is the upstream publication inventory. This script:
1. fetches and validates the public author profile,
2. writes a deterministic JSON snapshot,
3. renders the recent-publications block in index.html, and
4. writes a review report comparing Scholar with the curated LaTeX CV.

The CV is deliberately not rewritten from abbreviated Scholar metadata. The
scheduled workflow opens a pull request so Scholar/CV differences can be
reviewed before publication.
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
import re
import sys
import unicodedata
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SCHOLAR_USER = "oY_qRxMAAAAJ"
PROFILE_URL = (
    "https://scholar.google.com/citations"
    f"?user={SCHOLAR_USER}&hl=en&pagesize=100"
)
USER_AGENT = (
    "Mozilla/5.0 (compatible; FengbeiLiuAcademicProfileSync/1.0; "
    "+https://github.com/lfb-1/lfb-1.github.io)"
)
MIN_EXPECTED_RECORDS = 10
DISPLAY_COUNT = 6
# Preserve deliberate homepage exclusions from the previous CV-to-news workflow.
HOMEPAGE_EXCLUDE_TITLE_FRAGMENTS = ("CT-LVEF study",)
START_MARKER = "<!-- PUBLICATIONS_AUTO:START -->"
END_MARKER = "<!-- PUBLICATIONS_AUTO:END -->"


@dataclass(frozen=True)
class Publication:
    scholar_id: str
    title: str
    authors: str
    venue: str
    year: int | None
    citations: int
    url: str


class ScholarProfileParser(HTMLParser):
    """Extract publication rows from a Google Scholar author-profile page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.publications: list[Publication] = []
        self._row: dict[str, object] | None = None
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._gray_values: list[str] = []
        self._suppress_depth = 0

    @staticmethod
    def _classes(attrs: list[tuple[str, str | None]]) -> set[str]:
        values = dict(attrs).get("class") or ""
        return set(values.split())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = self._classes(attrs)
        attr_map = dict(attrs)

        if tag == "tr" and "gsc_a_tr" in classes:
            self._row = {}
            self._gray_values = []
            return
        if self._row is None:
            return

        if self._capture and self._suppress_depth:
            self._suppress_depth += 1
            return
        if self._capture == "gray" and "gs_oph" in classes:
            self._suppress_depth = 1
            return

        if tag == "a" and "gsc_a_at" in classes:
            self._row["href"] = attr_map.get("href") or ""
            self._begin_capture("title")
        elif tag == "div" and "gs_gray" in classes:
            self._begin_capture("gray")
        elif tag == "a" and "gsc_a_ac" in classes:
            self._begin_capture("citations")
        elif tag == "span" and "gsc_a_h" in classes:
            self._begin_capture("year")

    def handle_endtag(self, tag: str) -> None:
        if self._row is None:
            return

        if self._capture and self._suppress_depth:
            self._suppress_depth -= 1
            return

        ends_capture = (
            (self._capture == "title" and tag == "a")
            or (self._capture == "gray" and tag == "div")
            or (self._capture == "citations" and tag == "a")
            or (self._capture == "year" and tag == "span")
        )
        if ends_capture:
            value = " ".join("".join(self._buffer).split())
            field = self._capture
            assert field is not None
            if field == "gray":
                self._gray_values.append(value)
            else:
                self._row[field] = value
            self._capture = None
            self._buffer = []

        if tag == "tr":
            self._finish_row()

    def handle_data(self, data: str) -> None:
        if self._capture and not self._suppress_depth:
            self._buffer.append(data)

    def _begin_capture(self, field: str) -> None:
        self._capture = field
        self._buffer = []
        self._suppress_depth = 0

    def _finish_row(self) -> None:
        assert self._row is not None
        title = str(self._row.get("title", "")).strip()
        href = str(self._row.get("href", "")).strip()
        if title and href:
            query = parse_qs(urlparse(href).query)
            citation_key = query.get("citation_for_view", [""])[0]
            scholar_id = citation_key.split(":", 1)[-1] if citation_key else ""
            year_text = str(self._row.get("year", "")).strip()
            citation_text = str(self._row.get("citations", "")).strip()
            self.publications.append(
                Publication(
                    scholar_id=scholar_id,
                    title=title,
                    authors=self._gray_values[0] if self._gray_values else "",
                    venue=self._gray_values[1] if len(self._gray_values) > 1 else "",
                    year=int(year_text) if year_text.isdigit() else None,
                    citations=int(citation_text) if citation_text.isdigit() else 0,
                    url=urljoin("https://scholar.google.com", href),
                )
            )
        self._row = None
        self._capture = None
        self._buffer = []
        self._gray_values = []
        self._suppress_depth = 0


def parse_profile(html: str) -> list[Publication]:
    parser = ScholarProfileParser()
    parser.feed(html)
    return parser.publications


def fetch_profile(url: str = PROFILE_URL, timeout: int = 30) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Unable to fetch Google Scholar profile: {exc}") from exc


def load_previous_count(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        raise RuntimeError(f"Existing Scholar snapshot is unreadable: {path}: {exc}") from exc
    publications = payload.get("publications")
    if not isinstance(publications, list):
        raise RuntimeError(
            f"Existing Scholar snapshot has no publications list: {path}"
        )
    return len(publications)


def validate_profile(records: list[Publication], previous_count: int) -> None:
    minimum = MIN_EXPECTED_RECORDS
    if previous_count:
        minimum = max(minimum, int(previous_count * 0.75))
    if len(records) < minimum:
        raise RuntimeError(
            f"Scholar returned {len(records)} records; expected at least {minimum}. "
            "Refusing to replace the existing snapshot with a partial or blocked response."
        )

    ids = [record.scholar_id for record in records]
    if any(not value for value in ids):
        raise RuntimeError("At least one Scholar record has no citation identifier.")
    if len(ids) != len(set(ids)):
        raise RuntimeError("Scholar response contains duplicate citation identifiers.")

    wrong_profile = []
    for record in records:
        query = parse_qs(urlparse(record.url).query)
        citation_key = query.get("citation_for_view", [""])[0]
        if not citation_key.startswith(f"{SCHOLAR_USER}:"):
            wrong_profile.append(record.scholar_id)
    if wrong_profile:
        raise RuntimeError(
            "Scholar response contains citation identifiers from the wrong profile: "
            + ", ".join(wrong_profile[:3])
        )

    author_count = sum(bool(record.authors) for record in records)
    year_count = sum(record.year is not None for record in records)
    venue_count = sum(bool(record.venue) for record in records)
    minimum_venue_count = int(len(records) * 0.8)
    if author_count != len(records) or year_count != len(records) or venue_count < minimum_venue_count:
        raise RuntimeError(
            "Scholar metadata coverage is unexpectedly incomplete: "
            f"authors={author_count}/{len(records)}, years={year_count}/{len(records)}, "
            f"venues={venue_count}/{len(records)}. Refusing to publish a likely partial parse."
        )


def publication_sort_key(record: Publication) -> tuple[object, ...]:
    first_author = bool(
        re.match(r"^F(?:engbei)?\s+Liu\b", record.authors, re.IGNORECASE)
    )
    return (
        -(record.year or 0),
        not first_author,
        -record.citations,
        record.title.casefold(),
        record.scholar_id,
    )


def snapshot_payload(records: Iterable[Publication]) -> dict[str, object]:
    ordered = sorted(records, key=publication_sort_key)
    return {
        "schema_version": 1,
        "scholar_user": SCHOLAR_USER,
        "profile_url": PROFILE_URL,
        "publications": [asdict(record) for record in ordered],
    }


def write_snapshot(path: Path, records: list[Publication]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(snapshot_payload(records), indent=2, ensure_ascii=False) + "\n"
    path.write_text(content, encoding="utf-8")


def render_publication(record: Publication) -> str:
    year = str(record.year) if record.year else "—"
    return (
        '          <li class="publication">\n'
        f'            <span class="publication-year">{escape(year)}</span>\n'
        "            <div>"
        f'<a class="publication-title" href="{escape(record.url, quote=True)}" '
        f'target="_blank" rel="noopener">{escape(record.title)}</a>'
        f'<span class="publication-authors">{escape(record.authors)}</span>'
        f'<span class="publication-venue">{escape(record.venue)}</span></div>\n'
        "          </li>"
    )


def update_homepage(path: Path, records: list[Publication]) -> None:
    content = path.read_text(encoding="utf-8")
    if START_MARKER not in content or END_MARKER not in content:
        raise RuntimeError(f"Publication markers are missing from {path}")
    eligible = [
        record
        for record in records
        if not any(
            fragment.casefold() in record.title.casefold()
            for fragment in HOMEPAGE_EXCLUDE_TITLE_FRAGMENTS
        )
    ]
    selected = sorted(eligible, key=publication_sort_key)[:DISPLAY_COUNT]
    block = "\n".join(render_publication(record) for record in selected)
    pattern = re.compile(
        rf"({re.escape(START_MARKER)}\n).*?(\n\s*{re.escape(END_MARKER)})",
        flags=re.DOTALL,
    )
    updated, count = pattern.subn(rf"\1{block}\2", content)
    if count != 1:
        raise RuntimeError(f"Expected one publication block in {path}; found {count}")
    path.write_text(updated, encoding="utf-8")


def normalize_title(title: str) -> str:
    value = unicodedata.normalize("NFKD", title).casefold()
    value = value.replace("–", "-").replace("—", "-")
    return " ".join(re.findall(r"[a-z0-9]+", value))


def load_cv_publications(path: Path) -> list[dict[str, object]]:
    module_path = ROOT / "cv" / "generate_news.py"
    spec = importlib.util.spec_from_file_location("generate_news", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load CV parser from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    tex_content = path.read_text(encoding="utf-8")
    records = module.parse_publications(tex_content)
    for record in records:
        record["entry_type"] = "publication"

    # Preprints are intentionally omitted from the legacy homepage-news parser,
    # but they must count when auditing the complete CV against Scholar.
    index = 0
    while True:
        position = tex_content.find("\\resumeArxivheading{", index)
        if position == -1:
            break
        title_raw, after_title = module.extract_brace_arg(tex_content, position)
        authors_raw, after_authors = module.extract_brace_arg(tex_content, after_title)
        venue_raw, index = module.extract_brace_arg(tex_content, after_authors)
        venue = module.strip_latex(venue_raw)
        year_match = re.search(r"(20\d{2})", venue)
        records.append(
            {
                "title": module.strip_latex(title_raw),
                "authors": module.strip_latex(authors_raw),
                "venue": venue,
                "year": year_match.group(1) if year_match else "",
                "first_author": module.is_first_author(authors_raw),
                "qualifiers": [],
                "entry_type": "preprint",
            }
        )
    return records


def group_by_normalized_title(
    records: Iterable[Publication],
) -> dict[str, list[Publication]]:
    groups: dict[str, list[Publication]] = {}
    for record in records:
        groups.setdefault(normalize_title(record.title), []).append(record)
    return groups


def preferred_version(records: list[Publication]) -> Publication:
    """Prefer a publication record over a preprint, then the higher-cited record."""
    return min(
        records,
        key=lambda record: (
            "preprint" in record.venue.casefold(),
            -record.citations,
            publication_sort_key(record),
        ),
    )


def unique_by_normalized_title(records: Iterable[Publication]) -> list[Publication]:
    """Collapse Scholar preprint/journal duplicates for the CV inventory audit."""
    return [
        preferred_version(group)
        for group in group_by_normalized_title(records).values()
    ]


def duplicate_title_groups(records: Iterable[Publication]) -> list[list[Publication]]:
    groups = [
        sorted(group, key=publication_sort_key)
        for group in group_by_normalized_title(records).values()
        if len(group) > 1
    ]
    return sorted(groups, key=lambda group: publication_sort_key(group[0]))


def match_inventory(
    scholar_records: Iterable[Publication], cv_records: list[dict[str, object]]
) -> tuple[
    list[tuple[Publication, dict[str, object], float]],
    list[Publication],
    list[dict[str, object]],
]:
    scholar = sorted(
        unique_by_normalized_title(scholar_records), key=publication_sort_key
    )
    unmatched_scholar = set(range(len(scholar)))
    unmatched_cv = set(range(len(cv_records)))
    matches: list[tuple[Publication, dict[str, object], float]] = []

    cv_by_title: dict[str, list[int]] = {}
    for cv_index, cv_record in enumerate(cv_records):
        cv_by_title.setdefault(normalize_title(str(cv_record["title"])), []).append(
            cv_index
        )

    # Exact normalized-title matches are unambiguous and take priority.
    for scholar_index, publication in enumerate(scholar):
        key = normalize_title(publication.title)
        candidates = [index for index in cv_by_title.get(key, []) if index in unmatched_cv]
        if candidates:
            cv_index = candidates[0]
            matches.append((publication, cv_records[cv_index], 1.0))
            unmatched_scholar.remove(scholar_index)
            unmatched_cv.remove(cv_index)

    # Resolve remaining fuzzy candidates globally by descending similarity rather
    # than making the result depend on Scholar iteration order.
    fuzzy_candidates: list[tuple[float, int, int]] = []
    for scholar_index in unmatched_scholar:
        scholar_title = normalize_title(scholar[scholar_index].title)
        for cv_index in unmatched_cv:
            cv_title = normalize_title(str(cv_records[cv_index]["title"]))
            ratio = difflib.SequenceMatcher(None, scholar_title, cv_title).ratio()
            if ratio >= 0.82:
                fuzzy_candidates.append((ratio, scholar_index, cv_index))
    fuzzy_candidates.sort(
        key=lambda item: (
            -item[0],
            publication_sort_key(scholar[item[1]]),
            normalize_title(str(cv_records[item[2]]["title"])),
        )
    )
    for ratio, scholar_index, cv_index in fuzzy_candidates:
        if scholar_index not in unmatched_scholar or cv_index not in unmatched_cv:
            continue
        matches.append((scholar[scholar_index], cv_records[cv_index], ratio))
        unmatched_scholar.remove(scholar_index)
        unmatched_cv.remove(cv_index)

    matches.sort(key=lambda item: publication_sort_key(item[0]))
    scholar_only = [scholar[index] for index in sorted(unmatched_scholar)]
    cv_only = [cv_records[index] for index in sorted(unmatched_cv)]
    return matches, scholar_only, cv_only


def write_sync_report(
    path: Path,
    scholar_records: list[Publication],
    cv_records: list[dict[str, object]],
) -> None:
    matches, scholar_only, cv_only = match_inventory(scholar_records, cv_records)
    fuzzy_matches = [match for match in matches if match[2] < 1.0]
    duplicate_groups = duplicate_title_groups(scholar_records)
    lines = [
        "# Google Scholar ↔ CV sync report",
        "",
        "Generated by `scripts/sync_scholar.py`. Google Scholar is the upstream publication inventory; the LaTeX CV remains the curated presentation layer because Scholar abbreviates authors and may merge publication versions.",
        "",
        "## Summary",
        "",
        f"- Google Scholar records: {len(scholar_records)}",
        f"- CV entries (publications and preprints): {len(cv_records)}",
        f"- Matched titles: {len(matches)}",
        f"- Fuzzy title matches requiring review: {len(fuzzy_matches)}",
        f"- Scholar duplicate-version groups: {len(duplicate_groups)}",
        f"- Scholar-only titles requiring CV review: {len(scholar_only)}",
        f"- CV-only titles requiring Scholar review: {len(cv_only)}",
        "",
        "## Scholar-only titles",
        "",
    ]
    if scholar_only:
        lines.extend(
            f"- [{record.title}]({record.url}) — {record.venue or 'venue unavailable'}"
            for record in scholar_only
        )
    else:
        lines.append("- None.")
    lines.extend(["", "## CV-only titles", ""])
    if cv_only:
        lines.extend(
            f"- {record['title']} — {record['venue']} {record['year']}"
            for record in cv_only
        )
    else:
        lines.append("- None.")

    lines.extend(["", "## Fuzzy title matches", ""])
    if fuzzy_matches:
        lines.extend(
            f"- Scholar: [{publication.title}]({publication.url}) → CV: {cv_record['title']} (similarity {ratio:.3f})"
            for publication, cv_record, ratio in fuzzy_matches
        )
    else:
        lines.append("- None.")

    lines.extend(["", "## Scholar duplicate versions", ""])
    if duplicate_groups:
        for group in duplicate_groups:
            lines.append(f"- **{group[0].title}**")
            lines.extend(
                f"  - [{record.venue or 'venue unavailable'}]({record.url}); {record.citations} citations"
                for record in group
            )
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Review rule",
            "",
            "Do not copy Scholar metadata into the CV without review. Resolve true inventory differences, preserve full author names and venue qualifiers in `cv/fbl_cv.tex`, rebuild both PDF copies, then rerun this script before merging the synchronization pull request.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--html",
        type=Path,
        help="Parse a saved Scholar HTML page instead of fetching the live profile.",
    )
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html = (
        args.html.read_text(encoding="utf-8")
        if args.html
        else fetch_profile(timeout=args.timeout)
    )
    records = parse_profile(html)
    snapshot_path = ROOT / "data" / "scholar.json"
    validate_profile(records, load_previous_count(snapshot_path))

    cv_records = load_cv_publications(ROOT / "cv" / "fbl_cv.tex")
    write_snapshot(snapshot_path, records)
    update_homepage(ROOT / "index.html", records)
    write_sync_report(ROOT / "data" / "sync_report.md", records, cv_records)
    print(
        f"Synchronized {len(records)} Scholar records; "
        f"rendered {DISPLAY_COUNT} recent publications."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
