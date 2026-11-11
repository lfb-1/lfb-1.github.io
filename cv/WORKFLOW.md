# CV Workflow

## Canonical files

- `fbl_cv.tex` — curated CV source
- `fbl_cv.pdf` — compiled CV in this directory
- `../static/fbl_cv.pdf` — PDF served at the existing `/fbl_cv.pdf` URL
- `UPDATE_LOG.md` — historical record

Google Scholar is the upstream publication inventory. The CV remains the curated presentation layer because Scholar can abbreviate authors, merge versions, and omit venue qualifiers. See [`../SYNC.md`](../SYNC.md) for the complete synchronization contract.

## Publication update procedure

1. Add or correct the publication on the Google Scholar profile. For an author-confirmed paper not yet indexed, follow `../SYNC.md` without inventing missing metadata.
2. Run `python scripts/sync_scholar.py` from the repository root, or start the **Sync Google Scholar** Action.
3. Review `data/sync_report.md`.
4. For valid Scholar-only records, edit `fbl_cv.tex` with full author names and precise venue information.
5. Compile the CV and run `python3 scripts/publish_cv.py` from the repository root to copy the PDF into `static/` and refresh its links in `config.yml`.
6. Rerun the sync and tests.
7. Record the update in `UPDATE_LOG.md`. Curated homepage news is maintained in `config.yml` with the author-update date, not a guessed publication month.
8. Merge only after the Scholar/CV differences are understood.

## Build and verification

```bash
# From the vault root
just build-cv

# Or manually from Homepage/
(cd cv && pdflatex -interaction=nonstopmode -halt-on-error fbl_cv.tex)
python3 scripts/publish_cv.py
python3 -m unittest discover -s tests -p "test_*.py"
cmp cv/fbl_cv.pdf static/fbl_cv.pdf
hugo --minify --panicOnWarning
```

## Logging template

```markdown
## YYYY-MM-DD: [Type of Update]

**Updated By:** Agent

### Changes Made
- ✅ [Change]
  - Source: [URL or source description]

### Files Updated
- ✅ fbl_cv.tex
- ✅ fbl_cv.pdf
- ✅ ../static/fbl_cv.pdf
- ✅ ../config.yml (versioned CV links)
```
