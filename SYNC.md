# Homepage, CV, and Google Scholar synchronization

## Data flow

Google Scholar is the upstream publication inventory. The LaTeX CV remains curated because Scholar can abbreviate authors, merge versions, and omit venue details.

```text
Google Scholar public profile
          │
          ▼
scripts/sync_scholar.py
          ├── data/scholar.json       tracked snapshot
          └── data/sync_report.md     Scholar ↔ CV review
                                            │
                                            ▼
                                   cv/fbl_cv.tex + PDF
                                            │
                                   scripts/publish_cv.py
                                            ├── static/fbl_cv.pdf
                                            └── config.yml CV link versions

config.yml (profile + curated news) + content/ + layouts/ + assets/ + static/
          │
          ▼
         Hugo → public/ → GitHub Pages
```

Scholar synchronization writes only the snapshot and comparison report. It does not edit Hugo configuration, news, templates, or the public CV. The homepage has no Publications section. The script reads the public Scholar profile; it cannot edit that profile.

## Author-confirmed updates and news

A publication confirmed by the author can be added to `cv/fbl_cv.tex` before Scholar indexes it. Keep the supplied full title and authors. Leave an unconfirmed publication year or DOI blank; do not fabricate a Scholar record or citation ID. Confirmed journal entries without a year remain in the CV inventory and are reported as CV-only when absent from the snapshot.

`Recent News` is curated in `config.yml` under `params.news`, newest first. Both the homepage and `/news/` render this list. Dates are announcement dates supported by author updates or `cv/UPDATE_LOG.md`, not estimated publication or acceptance months. `cv/generate_news.py` remains the CV parser; its legacy approximate-date HTML output is not used by Hugo.

The saved Scholar snapshot keeps its provenance. Regenerating a report from that snapshot is not a live Scholar refresh.

## Scheduled workflow

`.github/workflows/sync-scholar.yml` runs monthly and can be started manually. It runs offline tests, fetches one profile page, rejects blocked or partial responses, refreshes the snapshot, compares it with the CV, and opens or updates a draft `automation/scholar-sync` pull request.

Repository settings must allow GitHub Actions to create pull requests. No API secret is required. Pull requests affecting the sync run only offline tests with read-only permissions; they never fetch Scholar or create another PR.

## Reviewing a sync pull request

Review `data/sync_report.md`:

- **Scholar-only:** add the work to the curated CV if appropriate, preserving full author names and precise venue qualifiers; otherwise correct the Scholar profile.
- **CV-only:** reconcile the missing Scholar record or correct the CV after checking the source.
- **Fuzzy title matches:** confirm that both titles refer to the same work.
- **Duplicate versions:** inspect the reported versions and retain the appropriate CV entry.

After editing the CV:

```bash
# From the vault root (build and publish the PDF)
just build-cv

# Or from Homepage/
(cd cv && pdflatex -interaction=nonstopmode -halt-on-error fbl_cv.tex)
python3 scripts/publish_cv.py

# Verify before committing
python3 -m unittest discover -s tests -p 'test_*.py'
cmp cv/fbl_cv.pdf static/fbl_cv.pdf
hugo --minify --panicOnWarning
```

`publish_cv.py` preserves the public `/fbl_cv.pdf` URL and updates all versioned CV links in `config.yml` using the first eight SHA-256 characters. Include the PDF and configuration together in the commit. Rerun the Scholar comparison when publication metadata changes, and merge only after the differences are understood.

## Local synchronization

```bash
python3 scripts/sync_scholar.py
# Or parse a saved complete profile without network access:
python3 scripts/sync_scholar.py --html /path/to/scholar.html
```

Snapshot and report output is deterministic; unchanged Scholar content causes no timestamp-only diffs.

## Recovering from a blocked fetch

HTTP 403/429 means Scholar refused access. The script exits **78 (failure)**, preserves existing files, and adds a blocked/stale Actions summary. Verification and PR creation are skipped. This does not count as a refresh. Do not repeatedly rerun, rotate identities/proxies, or bypass a CAPTCHA.

A supported recovery uses a fresh, complete HTML copy of the author's public profile (`oY_qRxMAAAAJ`) obtained through normal permitted browser access:

1. Open the profile URL from `scripts/sync_scholar.py`. Stop if ordinary access is denied. Otherwise show all publication rows and save the rendered HTML, excluding consent pages or CAPTCHAs.
2. Keep that HTML outside the repository.
3. On a review branch run `python3 scripts/sync_scholar.py --html /path/to/scholar.html`. The importer makes no network request and applies the same profile, record-count, duplicate-ID, and metadata checks. Invalid input fails before writing the snapshot or report. Check completeness manually as well.
4. Run the tests and inspect `data/scholar.json` and `data/sync_report.md`. Hugo sources and CV files should be unchanged. Open a draft review PR without auto-merging or restoring withdrawn entries.

A saved-HTML import does not establish that the next scheduled live fetch will succeed.
