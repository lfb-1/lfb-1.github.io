# Homepage Status

## Phase: Website and CV maintenance
## Priority: MEDIUM
## Last Updated: 2026-11-11

## Current State

- This directory is the `lfb-1/lfb-1.github.io` Git submodule. `index.html` and `style.css` define the public academic homepage.
- Added **Deep Learning With Longitudinal Electrocardiograms Predicts Atrial Fibrillation Better Than a Single Electrocardiogram** to the homepage and the CV's co-author publications. The author confirmed **JACC: Advances**, published; the author order is Sunwoo Kwak, Fengbei Liu, Nusrat Binta Nizam, Peter Okin, Mert R. Sabuncu.
- Publication year and DOI remain unfilled because they were not supplied or independently verified. The homepage uses a `New` label for this entry.
- `Recent News` follows About and precedes Recent publications. It includes the new JACC: Advances paper, MIDL 2027 Area Chair service, and MAdam's NeurIPS 2026 acceptance. Dates are announcement dates supported by the author's update and `cv/UPDATE_LOG.md`.
- The CV remains four pages. `cv/fbl_cv.pdf` and the public `fbl_cv.pdf` are identical; the homepage PDF link has a content-based cache version.
- Existing CV edits, including MIDL 2027 Area Chair service and removal of Research Interests, are preserved.
- Author-confirmed publications can be pinned outside the Scholar-generated block. The sync skips pinned titles to prevent duplicates, and its CV inventory retains confirmed journal papers without a year. See `SYNC.md`.
- The saved Scholar inventory was preserved. The comparison report records the new paper as CV-only pending Scholar indexing; no live Scholar refresh is claimed.
- Local verification passed: 22 unit tests, CV compilation without warnings or overflow, matching PDF copies, and 1440 / 768 / 390 px browser checks. See `data/homepage_update_2026-11-11.json`.

## Next Actions

- [ ] Add the publication year and DOI when confirmed by the author or publisher.
- [ ] Review the next Scholar sync and reconcile this author-confirmed publication when indexed.

## Important Paths

- `index.html`, `style.css`: homepage content and layout.
- `cv/fbl_cv.tex`: canonical CV source; `cv/UPDATE_LOG.md`: update history.
- `cv/fbl_cv.pdf`, `fbl_cv.pdf`: matching CV PDF copies.
- `SYNC.md`, `cv/WORKFLOW.md`: publication maintenance workflow.
- `data/scholar.json`, `data/sync_report.md`: saved Scholar inventory and comparison with the CV.
