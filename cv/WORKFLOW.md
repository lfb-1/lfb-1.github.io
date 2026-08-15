# CV Workflow

## Canonical files

- `fbl_cv.tex` — curated CV source
- `fbl_cv.pdf` — compiled CV in this directory
- `../fbl_cv.pdf` — PDF served by GitHub Pages
- `UPDATE_LOG.md` — historical record

Google Scholar is the upstream publication inventory. The CV remains the curated presentation layer because Scholar can abbreviate authors, merge versions, and omit venue qualifiers. See [`../SYNC.md`](../SYNC.md) for the complete synchronization contract.

## Publication update procedure

1. Add or correct the publication on the Google Scholar profile.
2. Run `python scripts/sync_scholar.py` from the repository root, or start the **Sync Google Scholar** Action.
3. Review `data/sync_report.md`.
4. For valid Scholar-only records, edit `fbl_cv.tex` with full author names and precise venue information.
5. Compile the CV and copy the PDF to the repository root.
6. Rerun the sync and tests.
7. Record the update in `UPDATE_LOG.md`.
8. Merge only after the Scholar/CV differences are understood.

## Build and verification

```bash
# From the vault root
just build-cv

# Or manually from Homepage/
cd cv
pdflatex -interaction=nonstopmode fbl_cv.tex
cp fbl_cv.pdf ../fbl_cv.pdf
cd ..
python scripts/sync_scholar.py
python -m unittest discover -s tests -p "test_*.py"
cmp cv/fbl_cv.pdf fbl_cv.pdf
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
- ✅ ../fbl_cv.pdf
```
