# Homepage, CV, and Google Scholar synchronization

## Data flow

Google Scholar is the upstream publication inventory:

```text
Google Scholar public profile
          │
          ▼
scripts/sync_scholar.py
          │
          ├── data/scholar.json       tracked snapshot
          ├── index.html              recent publications
          └── data/sync_report.md     Scholar ↔ CV review
                                            │
                                            ▼
                                   cv/fbl_cv.tex + PDFs
```

The sync is intentionally review-gated. Google Scholar author lists may be abbreviated, publication and preprint versions may be merged or duplicated, and venue details can be incomplete. The script therefore uses Scholar to determine the publication inventory and to render the homepage, while preserving the LaTeX CV as the curated presentation layer.

The workflow reads the public profile; it cannot edit the Google Scholar profile. Add or correct a publication in Google Scholar first, then let the workflow propagate the change into a review pull request.

## Scheduled workflow

`.github/workflows/sync-scholar.yml` runs monthly and can also be started manually from the Actions tab. It:

1. runs parser unit tests;
2. fetches one author-profile page;
3. rejects blocked or unexpectedly partial responses;
4. refreshes the tracked Scholar snapshot;
5. regenerates the homepage publication list;
6. compares Scholar titles with the CV;
7. opens or updates `automation/scholar-sync` as a pull request.

Repository settings must allow GitHub Actions to create pull requests. No API secret is required for the current low-frequency public-profile fetch. If Google blocks GitHub-hosted runners, the workflow fails without replacing the previous snapshot.

## Reviewing a sync pull request

Read `data/sync_report.md` and classify each difference:

- **Scholar-only:** add the publication to `cv/fbl_cv.tex` if it belongs in the CV, keeping full author names and precise venue qualifiers; otherwise correct or remove it in Google Scholar.
- **CV-only:** add or restore the record in Google Scholar, or remove it from the CV if it should no longer be listed.
- **Fuzzy title matches:** confirm that the Scholar and CV titles refer to the same work; the report records both titles and their similarity score.
- **Duplicate versions:** inspect every version listed in the report, keep the appropriate version in the CV, and resolve the duplicate in Google Scholar when possible.

After any CV edit, rebuild and copy the PDF:

```bash
# From the vault root
just build-cv

# Or from this repository
cd cv
pdflatex -interaction=nonstopmode fbl_cv.tex
cp fbl_cv.pdf ../fbl_cv.pdf
```

Then rerun the sync and verify that the report reflects the intended state:

```bash
python scripts/sync_scholar.py
python -m unittest discover -s tests -p "test_*.py"
cmp cv/fbl_cv.pdf fbl_cv.pdf
```

Merge only after the homepage diff, CV source/PDF, and Scholar/CV report are consistent.

## Local use

Run the live synchronization:

```bash
python scripts/sync_scholar.py
```

For parser debugging with a saved response:

```bash
python scripts/sync_scholar.py --html /path/to/scholar.html
```

The JSON snapshot and report are deterministic: when Scholar content has not changed, rerunning the script does not create timestamp-only diffs.


## Recovering from a blocked fetch

HTTP 403/429 means Google Scholar refused the request, not that the parser or
unit tests failed. The sync exits **78 (failure)**, leaves tracked files alone,
and adds an explicit blocked/stale Actions summary. Verification and PR creation
are skipped. This is not a successful refresh and does not resolve Google's
external access restriction. Other network/parse errors remain failures too.
Do not repeatedly rerun, rotate identities/proxies, or attempt to bypass a CAPTCHA.

A supported recovery needs a **fresh, complete HTML copy of this author's public
profile** (`oY_qRxMAAAAJ`), obtained through normal permitted browser access:

1. Open the profile URL in `scripts/sync_scholar.py`. If ordinary access is denied,
   stop; do not bypass the restriction. If accessible, show all publication rows
   and save the rendered page HTML (not a screenshot, consent page, or CAPTCHA).
2. Keep the saved HTML outside the repository; it need not be published.
3. On a review branch, run
   `python scripts/sync_scholar.py --html /path/to/scholar.html`.
   This makes **no network request** and applies the same profile, record-count,
   duplicate-ID and metadata checks as a live fetch. Incomplete inputs fail
   before modifying the snapshot, homepage or report. Review the record inventory
   yourself too: count thresholds cannot prove completeness.
4. Run `python -m unittest discover -s tests -p "test_*.py"` and inspect the
   diffs of `data/scholar.json`, `index.html`, and `data/sync_report.md`. Open a
   draft review PR; do not auto-merge or add back deliberately withdrawn entries.

The CV and its PDFs are never rewritten by this importer. A saved-HTML refresh
is a manual recovery, not proof that the next scheduled live fetch will work.
Pull requests affecting the sync run only offline tests with read-only permissions;
they never fetch Scholar or create another PR.
