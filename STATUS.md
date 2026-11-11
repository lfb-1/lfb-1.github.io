# Homepage Status

## Phase: Hugo website and CV maintenance
## Priority: MEDIUM
## Last Updated: 2026-11-11

## Current State

- This directory is the `lfb-1/lfb-1.github.io` Git submodule. The author chose a full migration to Pascal Michaillat's **hugo-website**, using its vendored PaperMod theme. The previous unpublished Minimal Light adaptation was discarded.
- `config.yml`, `content/`, `layouts/`, and `assets/` define the site. The homepage uses the minimal profile layout with curated **Recent News**, contact icons, and CV access. There is no homepage Publications section. Experience and Academic Service have separate Markdown pages.
- GitHub Pages is configured through `.github/workflows/hugo.yml`: tests, a pinned **Hugo Extended 0.169.0** build, and artifact deployment. Pull requests validate without deploying. Only Hugo's `public/` output is published.
- `cv/fbl_cv.pdf` and `static/fbl_cv.pdf` are identical four-page PDFs; their contents are unchanged by the migration. The public `/fbl_cv.pdf` and `/thesis/ElsnerTalk.pdf` addresses are preserved. `scripts/publish_cv.py` copies the compiled CV and updates the SHA-256 cache version in `config.yml`.
- Scholar synchronization maintains only `data/scholar.json` and `data/sync_report.md`. It preserves the Hugo site, curated news, and public CV; it cannot restore a homepage publication list. No live Scholar refresh was performed for the migration.
- The CV retains **Deep Learning With Longitudinal Electrocardiograms Predicts Atrial Fibrillation Better Than a Single Electrocardiogram**, by Sunwoo Kwak, Fengbei Liu, Nusrat Binta Nizam, Peter Okin, and Mert R. Sabuncu. The author confirmed publication in **JACC: Advances**; publication year and DOI remain unfilled pending confirmation.
- Recent News dates are announcement dates, supported by the author's updates and `cv/UPDATE_LOG.md`. The three current entries concern the JACC: Advances paper, MIDL 2027 Area Chair service, and MAdam's NeurIPS 2026 acceptance.
- Local verification includes 18 unit tests, a warning-free production build, matching CV copies, and browser checks for desktop/mobile layout, all three subpages, CV access, and the existing thesis PDF URL. Deployment evidence is recorded in the Vault's `wiki/projects/homepage.md` after online verification.

## Next Actions

- [ ] Add the JACC: Advances publication year and DOI when confirmed by the author or publisher.
- [ ] Review the next Scholar sync and reconcile the author-confirmed publication when indexed.

## Important Paths

- `config.yml`: profile, navigation, contact links, versioned CV links, and curated news.
- `content/`: Markdown pages; `layouts/` and `assets/`: Hugo templates and styling.
- `.github/workflows/hugo.yml`: build validation and Pages deployment.
- `cv/fbl_cv.tex`: canonical CV source; `cv/UPDATE_LOG.md`: update history.
- `cv/fbl_cv.pdf`, `static/fbl_cv.pdf`: matching CV PDF copies.
- `scripts/publish_cv.py`, `SYNC.md`, `cv/WORKFLOW.md`: maintenance workflow.
- `data/scholar.json`, `data/sync_report.md`: saved Scholar inventory and CV comparison, excluded from the published site.
- `THIRD_PARTY_NOTICES.md`: pinned template provenance and included MIT licenses.
