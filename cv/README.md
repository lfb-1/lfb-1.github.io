# Fengbei Liu - Curriculum Vitae

This folder contains the most up-to-date CV for Fengbei Liu.

## Files

- `fbl_cv.tex` - LaTeX source file
- `fbl_cv.pdf` - Compiled PDF; kept identical to `../fbl_cv.pdf`
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

## Current Status (Last Updated: 2026-11-11)

**Position:** Postdoctoral Researcher at Cornell Tech, Cornell University (Feb 2024 - Present).

**Latest addition:** *Deep Learning With Longitudinal Electrocardiograms Predicts Atrial Fibrillation Better Than a Single Electrocardiogram*, by Sunwoo Kwak, Fengbei Liu, Nusrat Binta Nizam, Peter Okin, and Mert R. Sabuncu. The author confirmed publication in **JACC: Advances** on 2026-11-11. Publication year and DOI were not supplied or independently verified, so they remain blank.

The homepage now has a curated **Recent News** section. Dates there reflect announcement dates; publication entries retain their own verified metadata. `../data/sync_report.md` compares the saved Scholar inventory with the curated CV, including the new author-confirmed paper.

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
