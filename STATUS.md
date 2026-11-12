# Homepage Status

## Phase: Hugo website and CV maintenance
## Priority: MEDIUM
## Last Updated: 2026-11-12

## Current State

- This directory is the `lfb-1/lfb-1.github.io` Git submodule. The author chose a full migration to Pascal Michaillat's **hugo-website**, using its vendored PaperMod theme. The previous unpublished Minimal Light adaptation was discarded.
- `config.yml`, `content/`, `layouts/`, and `assets/` define the site. The homepage has a minimal profile, Recent News, contact icons, and a CV icon; the CV button and text navigation entry were removed. The research description is a separate paragraph: “My research lies at the intersection of computer vision, medical image analysis and deep learning.”
- Publications, News, Experience, and Academic Service have separate pages. `/publications/` includes every CV record: 38 published/accepted papers and two preprints, with author order, equal-contribution markers, venue qualifiers, and undated journal entries retained. The homepage contains only a Publications link, not the full list.
- GitHub Pages is configured through `.github/workflows/hugo.yml`: tests, a pinned **Hugo Extended 0.169.0** build, and artifact deployment. Pull requests validate without deploying. Only Hugo's `public/` output is published.
- `cv/fbl_cv.pdf` and `static/fbl_cv.pdf` are identical four-page PDFs; their contents are unchanged by the migration. The public `/fbl_cv.pdf` and `/thesis/ElsnerTalk.pdf` addresses are preserved. `scripts/publish_cv.py` copies the compiled CV and updates the SHA-256 cache version in `config.yml`.
- `scripts/sync_scholar.py` maintains the Scholar snapshot and CV report. The monthly workflow then regenerates `data/publications.json` from the curated CV, using matched Scholar records only for links. Hugo configuration, news, pages, templates, and the CV are preserved. No live Scholar refresh was performed for these site updates.
- The CV retains **Deep Learning With Longitudinal Electrocardiograms Predicts Atrial Fibrillation Better Than a Single Electrocardiogram**, by Sunwoo Kwak, Fengbei Liu, Nusrat Binta Nizam, Peter Okin, and Mert R. Sabuncu. The author confirmed publication in **JACC: Advances**; publication year and DOI remain unfilled pending confirmation.
- Recent News contains 18 entries spanning 2020–2026, with six shown on the homepage. Dates use confirmed announcement months where available, otherwise CV publication years; months are never estimated. The earlier CT-LVEF news exclusion remains; the full Publications page includes that paper.
- Local verification includes 20 unit tests, a warning-free production build, matching CV copies, desktop/tablet/mobile browser checks, all 40 publication entries, and 22 working news-to-publication anchors. Deployment evidence is recorded in the Vault's `wiki/projects/homepage.md` after online verification.

## Next Actions

- [ ] Add the JACC: Advances publication year and DOI when confirmed by the author or publisher.
- [ ] Review the next Scholar sync and reconcile the author-confirmed publication when indexed.

## Important Paths

- `config.yml`: profile, navigation, contact links, versioned CV links, and curated news.
- `content/`: Markdown pages; `layouts/` and `assets/`: Hugo templates and styling.
- `.github/workflows/hugo.yml`: build validation and Pages deployment.
- `cv/fbl_cv.tex`: canonical CV source; `cv/UPDATE_LOG.md`: update history.
- `cv/fbl_cv.pdf`, `static/fbl_cv.pdf`: matching CV PDF copies.
- `scripts/publish_cv.py`, `scripts/build_publications.py`, `SYNC.md`, `cv/WORKFLOW.md`: maintenance workflow.
- `data/publications.json`: complete CV-based publication-page data; checked for staleness during builds.
- `data/scholar.json`, `data/sync_report.md`: saved Scholar inventory and CV comparison, excluded from the published site.
- `THIRD_PARTY_NOTICES.md`: pinned template provenance and included MIT licenses.
