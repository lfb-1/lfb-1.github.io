# Fengbei Liu — academic website

Public site: <https://lfb-1.github.io/>

This is a Hugo site based on [Pascal Michaillat's hugo-website](https://github.com/pmichaillat/hugo-website) and its vendored PaperMod theme. It uses the template's minimal profile layout, with curated Recent News below the introduction. Experience and Academic Service are separate Markdown pages. The homepage has no publication list; Google Scholar and the CV provide the publication inventory.

## Edit and preview

Use **Hugo Extended 0.169.0**, the version pinned in `.github/workflows/hugo.yml`. No Node.js packages or theme downloads are required.

```bash
hugo server --disableFastRender
# Open http://localhost:1313/

# Production validation
hugo --minify --panicOnWarning
python3 -m unittest discover -s tests -p 'test_*.py'
cmp cv/fbl_cv.pdf static/fbl_cv.pdf
```

- `config.yml`: introduction, contact links, buttons, navigation, and `params.news`.
- `content/`: Markdown pages for News, Experience, and Service.
- `layouts/partials/index_profile.html`: profile layout and homepage news.
- `assets/css/extended/fengbei.css`: site-specific styling.
- `static/fbl_cv.pdf`: public CV, served at the existing `/fbl_cv.pdf` URL.
- `cv/fbl_cv.tex`: canonical CV source; see `cv/WORKFLOW.md`.
- `scripts/publish_cv.py`: copy a compiled CV and update the versioned links.
- `data/scholar.json`, `data/sync_report.md`: publication maintenance files; see `SYNC.md`.

Add news to `params.news` in `config.yml`, newest first. Dates describe the author's announcement, rather than an estimated acceptance or publication month. The homepage shows the first three entries; `/news/` shows all entries.

## Deployment

GitHub Pages uses **GitHub Actions**. Every push to `main` runs tests, builds with the pinned Hugo version, checks public files, uploads `public/`, and deploys that artifact. Pull requests run validation without deploying.

Only Hugo's output is published. CV sources, scripts, Scholar snapshots, and repository documentation are not copied into `public/`. The existing `/thesis/ElsnerTalk.pdf` URL is preserved through a static mount.

Build output (`public/`, `resources/`, `.hugo_build.lock`) is ignored. Do not edit generated HTML or recreate a root `index.html`.

## Third-party sources

Template and theme code are vendored for reproducible builds. See `THIRD_PARTY_NOTICES.md` and the included MIT licenses for provenance and local compatibility changes.
