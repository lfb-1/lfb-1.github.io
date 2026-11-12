# Fengbei Liu - Curriculum Vitae

This folder contains the most up-to-date CV for Fengbei Liu.

## Files

- `fbl_cv.tex` - LaTeX source file
- `fbl_cv.pdf` - Compiled PDF; kept identical to `../static/fbl_cv.pdf`
- `WORKFLOW.md` - Review-gated workflow for updating the CV
- `UPDATE_LOG.md` - History of CV updates
- `../SYNC.md` - Homepage, CV, and Google Scholar synchronization contract

## Quick Compile

```bash
just build-cv          # from the vault root
# or, manually:
(cd Homepage/cv && pdflatex -interaction=nonstopmode -halt-on-error fbl_cv.tex)
(cd Homepage && python3 scripts/publish_cv.py && python3 scripts/build_publications.py)
```

After commit + push inside `Homepage/`, GitHub Pages rebuilds automatically.

## Current Status (Last Updated: 2026-11-12)

**Position:** Postdoctoral Researcher at Cornell Tech, Cornell University (Feb 2024 - Present).

**Latest addition:** *Deep Learning With Longitudinal Electrocardiograms Predicts Atrial Fibrillation Better Than a Single Electrocardiogram*, by Sunwoo Kwak, Fengbei Liu, Nusrat Binta Nizam, Peter Okin, and Mert R. Sabuncu. The author confirmed publication in **JACC: Advances** on 2026-11-11. Publication year and DOI were not supplied or independently verified, so they remain blank.

The homepage's curated **Recent News** section is configured in `config.yml`; it shows six entries and `/news/` renders all 18 current entries. Dates use confirmed announcement months or CV publication years. `/publications/` includes all 40 CV records: 38 publications and two preprints. It is generated from `../data/publications.json`, with CV author order and status preserved. The CV remains available through the profile icon. `../data/sync_report.md` compares the saved Scholar inventory with the curated CV, including the author-confirmed JACC: Advances paper.

## Synchronization Schedule

The **Sync Google Scholar** GitHub Action runs monthly and opens a review pull request when the public Scholar profile changes. It refreshes the saved inventory and `../data/sync_report.md`, then regenerates the CV-based publication-page data. Configuration, news, Markdown pages, templates, and CV files are preserved. Review the differences and rebuild the PDF and publication data after editing the CV. See `../SYNC.md` for details.

Additional checks remain useful before major conference deadlines and when a preprint changes publication status.

## Contact Information

- **Email:** fl453@cornell.edu
- **Google Scholar:** https://scholar.google.com/citations?user=oY_qRxMAAAAJ&hl=en
- **OpenReview:** https://openreview.net/profile?id=~Fengbei_Liu1
- **ResearchGate:** https://www.researchgate.net/profile/Fengbei-Liu
- **LinkedIn:** https://www.linkedin.com/in/fengbei-liu-2bb11b177/
- **GitHub:** https://github.com/FBLADL?tab=repositories
- **Lab:** Sabuncu Lab, Cornell Tech

## Related Folders

- `../thesis/` — PhD thesis sources, also hosted in this Pages repo
- vault `Presentations/` — slide templates (ElsnerTalk.tex Beamer)
