#!/usr/bin/env python3
"""Build the complete publication-page inventory from the curated CV."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from sync_scholar import (
    Publication,
    load_cv_publications,
    match_inventory,
    normalize_title,
)

ROOT = Path(__file__).resolve().parents[1]
VENUES = {
    "IEEE TPAMI": (
        "IEEE Transactions on Pattern Analysis "
        "and Machine Intelligence (TPAMI)"
    ),
    "IEEE TIP": "IEEE Transactions on Image Processing (TIP)",
    "IEEE TMI": "IEEE Transactions on Medical Imaging (TMI)",
    "IEEE JBHI": "IEEE Journal of Biomedical and Health Informatics (JBHI)",
    "TMLR": "Transactions on Machine Learning Research (TMLR)",
}


def build_inventory(cv_path: Path, scholar_path: Path) -> dict:
    records = load_cv_publications(cv_path)
    if not records:
        raise RuntimeError("The CV contains no publication records.")
    snapshot = json.loads(scholar_path.read_text(encoding="utf-8"))
    scholar = [Publication(**row) for row in snapshot["publications"]]
    matches, _, _ = match_inventory(scholar, records)
    links = {
        normalize_title(str(cv["title"])): publication.url
        for publication, cv, _ in matches
    }
    publications = []
    seen = set()
    for record in records:
        title = str(record["title"])
        # Correct the CV's transposed letters using the verified Scholar title.
        if title.startswith("ACPL:"):
            title = title.replace("Psueod-labelling", "Pseudo-labelling")
        identifier = re.sub(
            r"[^a-z0-9]+", "-", normalize_title(title)
        ).strip("-")
        if identifier in seen:
            raise RuntimeError(f"Duplicate CV publication: {title}")
        seen.add(identifier)
        year = str(record["year"])
        venue = str(record["venue"])
        if record["entry_type"] == "preprint" and year:
            venue = re.sub(rf",?\s*{re.escape(year)}$", "", venue).strip()
        publications.append(
            {
                "id": identifier,
                "title": title,
                "authors": str(record["authors"]).replace(
                    "Fengbei Liu Davis", "Fengbei Liu, Davis"
                ),
                "venue": VENUES.get(venue, venue),
                "year": year,
                "kind": record["entry_type"],
                "qualifiers": record["qualifiers"],
                "url": links.get(normalize_title(str(record["title"])), ""),
            }
        )
    return {"source": "cv/fbl_cv.tex", "publications": publications}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the saved inventory is stale.",
    )
    args = parser.parse_args()
    payload = build_inventory(
        ROOT / "cv/fbl_cv.tex", ROOT / "data/scholar.json"
    )
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    destination = ROOT / "data/publications.json"
    if args.check:
        if not destination.exists() or destination.read_text() != content:
            raise RuntimeError(
                "Publication data is stale. "
                "Run python scripts/build_publications.py."
            )
    else:
        destination.write_text(content, encoding="utf-8")
    print(f"Verified {len(payload['publications'])} CV publication records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
