#!/usr/bin/env python3
"""Copy the compiled CV into Hugo's static directory and refresh CV links."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    pdf = (ROOT / "cv/fbl_cv.pdf").read_bytes()
    if not pdf.startswith(b"%PDF-"):
        raise RuntimeError(
            "cv/fbl_cv.pdf is not a PDF; rebuild it before publishing."
        )
    version = hashlib.sha256(pdf).hexdigest()[:8]
    config = ROOT / "config.yml"
    updated, count = re.subn(
        r"fbl_cv\.pdf\?v=[0-9a-f]+",
        f"fbl_cv.pdf?v={version}",
        config.read_text(encoding="utf-8"),
    )
    if not count:
        raise RuntimeError("config.yml has no versioned CV link to update.")
    destination = ROOT / "static/fbl_cv.pdf"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(pdf)
    config.write_text(updated, encoding="utf-8")
    print(
        f"Published static/fbl_cv.pdf; "
        f"updated {count} CV links (?v={version})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
