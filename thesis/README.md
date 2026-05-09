# PhD Thesis Materials

This folder contains materials related to the PhD thesis on Weakly-supervised Learning in Computer Vision and Medical Imaging.

## Contents

### Presentation Files
Multiple versions of thesis presentation (ElsnerTalk):
- `ElsnerTalk.tex` - LaTeX source for thesis presentation
- `ElsnerTalk.pdf` - Main presentation (latest version)
- `ElsnerTalk 2.pdf` through `ElsnerTalk 5.pdf` - Previous versions
- Supporting compilation files (.synctex.gz, .aux, etc.)

### Topic
**Weakly-supervised Learning in Computer Vision and Medical Imaging**

Presenter: Fengbei Liu
Institution: Australian Institute for Machine Learning (AIML), University of Adelaide
PhD Period: April 2020 - October 2023
Supervisors: Prof. Gustavo Carneiro, Prof. Mark Jenkinson

## File Structure

```
PhD_Thesis/
├── ElsnerTalk.tex          # Main presentation source
├── ElsnerTalk.pdf          # Latest compiled version
├── ElsnerTalk 2.pdf        # Version 2
├── ElsnerTalk 3.pdf        # Version 3
├── ElsnerTalk 4.synctex.gz # Version 4 auxiliary
├── ElsnerTalk 5.synctex.gz # Version 5 auxiliary
├── ElsnerTalk 6.synctex.gz # Version 6 auxiliary
└── figures/                # (if present) Image assets
```

## Versions

The numbered versions (2-6) represent iterations of the thesis presentation, likely created for:
- Thesis proposal
- Mid-candidature review
- Final thesis defense
- Conference presentations
- Other milestone presentations

## Usage

To recompile the presentation:

```bash
cd /Users/fengbeiliu/Documents/Vault/PhD_Thesis
pdflatex ElsnerTalk.tex
pdflatex ElsnerTalk.tex  # Run twice for references
```

---

**Last Updated:** 2026-01-19
**PhD Completed:** October 2023
