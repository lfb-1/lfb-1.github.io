# Third-party notices

## hugo-website

- Author: Pascal Michaillat
- Source: https://github.com/pmichaillat/hugo-website
- Imported revision: `96e8a60674cccb70556f164823397df4d14b8a4a` (2026-10-14)
- License: MIT, reproduced in `LICENSE-hugo-website.md`

The project-level `layouts/` and base `assets/css/` are adapted from this revision. The example content, sample CV, and sample profile image are not included. Local changes add the curated news section, adjust the profile for a vertical layout on desktop and mobile, and use Hugo's current language properties in `layouts/_default/baseof.html`.

## PaperMod

- Authors: nanxiaobei and adityatelange; maintained by adityatelange
- Source: https://github.com/adityatelange/hugo-PaperMod
- Imported as: `themes/PaperMod/` from the hugo-website revision above
- License: MIT, reproduced in `themes/PaperMod/LICENSE`

The vendored Open Graph template uses `site.Language.Locale` in place of the deprecated `site.Language.LanguageCode` for Hugo 0.169.0 compatibility. No external theme checkout is needed for deployment.
