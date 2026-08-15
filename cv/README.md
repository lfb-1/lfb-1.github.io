# Fengbei Liu - Curriculum Vitae

This folder contains the most up-to-date CV for Fengbei Liu.

## Files

- `fbl_cv.tex` - LaTeX source file
- `fbl_cv.pdf` - Compiled PDF (last updated: 2026-01-19, 3:00 PM)
- `WORKFLOW.md` - Review-gated workflow for updating the CV
- `UPDATE_LOG.md` - History of CV updates
- `../SYNC.md` - Homepage, CV, and Google Scholar synchronization contract

## Quick Compile

```bash
just build-cv          # from the vault root
# or, manually:
cd Homepage/cv && pdflatex -interaction=nonstopmode fbl_cv.tex && cp fbl_cv.pdf ../fbl_cv.pdf
```

After commit + push inside `Homepage/`, GitHub Pages rebuilds automatically.

## Current Status (Last Updated: 2026-01-19)

**Position:** Postdoctoral Researcher at Cornell Tech, Cornell University (Feb 2024 - Present)

**Recent Publications (2024-2025):**
- 2 papers in IEEE TMI (Transactions on Medical Imaging)
- 1 paper in IEEE TPAMI (Transactions on Pattern Analysis and Machine Intelligence)
- 1 paper in IEEE JBHI (IEEE Journal of Biomedical and Health Informatics)
- 1 paper in TMLR (Transactions on Machine Learning Research)
- 1 paper in Medical Image Analysis
- 1 paper at CVPR 2024

**Total 2025 Publications: 7 papers (4 in IEEE journals/transactions)**

**Citation Count:** 1,158+ (as of Jan 2026)

**Total Publications:** 48 papers

## Synchronization Schedule

The **Sync Google Scholar** GitHub Action runs monthly and opens a review pull request when the public Scholar profile changes. It refreshes the homepage publication list and writes `../data/sync_report.md`; it does not copy abbreviated Scholar metadata directly into the CV. Review Scholar/CV differences and rebuild both PDF copies before merging. See `../SYNC.md` for details.

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
