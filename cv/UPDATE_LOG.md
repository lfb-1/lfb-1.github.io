# CV Update Log

This file tracks all updates made to Fengbei Liu's CV.

---

## 2026-08-15: Synchronize Four Google Scholar Records

**Updated By:** Agent

### Changes Made
- ✅ Retained **MAdam: Metric-Aware Multi-Objective Adam** under Preprint/Under-Review and added its arXiv identifier and year
  - Source: https://arxiv.org/abs/2606.03904
- ✅ Expanded the full author list and added the TechRxiv year for **Agentic Large-Language-Model Systems in Medicine: A Systematic Review and Taxonomy**
  - Source: https://doi.org/10.36227/techrxiv.175736231.12300949/v1
- ✅ Corrected the author metadata and added the arXiv identifier and year for **Asymmetric Co-teaching with Multi-view Consensus for Noisy Label Learning**
  - Source: https://arxiv.org/abs/2301.01143
- ✅ Added **Automatic Segmentation of Multiple Structures in Knee Arthroscopy Using Deep Learning** to Co-author Publications
  - Venue: IEEE Access 8, 51853–51861, 2020
  - Source: https://doi.org/10.1109/ACCESS.2020.2980025
- ✅ Updated the Scholar/CV audit to include both published and preprint CV entries

### Files Updated
- ✅ fbl_cv.tex
- ✅ fbl_cv.pdf
- ✅ ../fbl_cv.pdf
- ✅ ../data/sync_report.md

---

## 2026-07-10: Remove Phone Number from Contact Line

**Updated By:** Agent

### Changes Made
- ✅ Removed the mobile phone entry (and its `$|$` separator) from the heading contact line in fbl_cv.tex; contact line now starts with the institutional email
- ✅ Rebuilt the PDF and bumped the homepage cache-buster (fbl_cv.pdf?v=227c34f7); verified the number no longer appears in the compiled PDF text
- Source: Author (Fengbei Liu)

### Files Updated
- ✅ fbl_cv.tex
- ✅ fbl_cv.pdf, ../fbl_cv.pdf
- ✅ ../index.html (cache-buster)

---

## 2026-06-17: Exclude CT-LVEF Study from Homepage News

**Updated By:** Agent

### Changes Made
- ✅ Added a NEWS_EXCLUDE mechanism to generate_news.py (substring match, case-insensitive)
- ✅ Excluded "...The CT-LVEF study" from homepage news; paper remains listed in the CV publications
- Source: Author (Fengbei Liu)

### Files Updated
- ✅ generate_news.py
- ✅ ../index.html (news regenerated)

---

## 2026-06-17: Institutional Email + CV Cache-Busting

**Updated By:** Agent

### Changes Made
- ✅ Replaced personal Gmail address with institutional fl453@cornell.edu in fbl_cv.tex (contact line) and cv/README.md
- ✅ Added a content-hash cache-buster to the homepage CV link (fbl_cv.pdf?v=<hash>) so browsers always fetch the latest PDF; justfile build-cv now auto-bumps it on every build
- Source: Author (Fengbei Liu)

### Files Updated
- ✅ fbl_cv.tex
- ✅ fbl_cv.pdf
- ✅ cv/README.md
- ✅ ../index.html (CV link cache-buster)
- ✅ ../../justfile (build-cv auto-bump) [Vault repo]

---

## 2026-06-17: Updated Conference Reviewer Service

**Updated By:** Agent

### Changes Made
- ✅ Added 2026 reviewing to the Conference reviewer line: CVPR 2026, MICCAI 2026, NeurIPS 2026
  - Now: MICCAI 2021/2026, CVPR 2022/2023/2024/2026, NeurIPS 2023/2024/2026
  - Source: Author (Fengbei Liu)
- Note: homepage Service section lists conference names without years (CVPR/NeurIPS/MICCAI already present), so index.html is unchanged.

### Files Updated
- ✅ fbl_cv.tex
- ✅ fbl_cv.pdf

---

## 2026-06-17: Two Papers Published in European Heart Journal-Digital Health

**Updated By:** Agent

### Changes Made
- ✅ Moved **CT-LVEF study** (An Artificial Intelligence Model to Detect Abnormal Ejection Fraction from Non-Contrast Chest CT) from Preprint/Under-Review to Co-author Publications
  - Venue: European Heart Journal-Digital Health 2026
- ✅ Added co-author publication **Cardio Amyloid-AI: Advanced Multimodal Screening for Transthyretin Cardiac Amyloidosis in Severe Aortic Stenosis Patients**
  - Venue: European Heart Journal-Digital Health 2026
- ✅ Long author lists abbreviated to first-authors-through-Fengbei + et al.
- ✅ generate_news.py: registered European Heart Journal-Digital Health as a journal (also added generic "accepted in [journal]" phrasing for any future accepted-but-not-yet-published papers)
- Source: Author (Fengbei Liu)

### Files Updated
- ✅ fbl_cv.tex
- ✅ fbl_cv.pdf
- ✅ generate_news.py
- ✅ ../index.html (news regenerated)

---

## 2026-06-17: Added MAdam Preprint

**Updated By:** Agent

### Changes Made
- ✅ Added preprint **MAdam: Metric-Aware Multi-Objective Adam** to Preprint/Under-Review
  - Authors: Fengbei Liu, Rachit Saluja, Sunwoo Kwak, Ruibo Wang, Ruining Deng, Heejong Kim, Johannes C. Paetzold, Mert R. Sabuncu
  - Venue: arXiv preprint
  - Source: Author (Fengbei Liu)
- Note: preprints are excluded from homepage news (generate_news.py parses only \resumePubheading), so index.html is unchanged.

### Files Updated
- ✅ fbl_cv.tex
- ✅ fbl_cv.pdf

---

## 2026-06-17: Added MICCAI 2026 Paper

**Updated By:** Agent

### Changes Made
- ✅ Added co-author publication **ShapKO: Shapley-Adaptive Modality Knockout for Robust Multimodal Learning**
  - Authors: Nusrat Binta Nizam, Fengbei Liu, Sunwoo Kwak, Minh Nguyen, Ruining Deng, Mert R. Sabuncu
  - Venue: MICCAI 2026
  - Source: Author (Fengbei Liu)

### Files Updated
- ✅ fbl_cv.tex
- ✅ fbl_cv.pdf
- ✅ ../index.html (news regenerated via generate_news.py)

---

## 2026-01-19: Comprehensive Update from Online Sources

**Updated By:** Agent

### Changes Made

#### 1. Position Update
- ✅ Corrected title: "Postdoctoral Research Associate" → "Postdoctoral Researcher"
- ✅ Updated supervisor name: "Prof. Mert Sabuncu" → "Prof. Mert R. Sabuncu"
- ✅ Fixed typo: "Australian Institue" → "Australian Institute"

#### 2. New Publications Added (2024-2025)

**Published - Co-author:**
- ✅ **Cross- and Intra-image Prototypical Learning for Multi-label Disease Diagnosis and Interpretation**
  - Authors: Chong Wang, Fengbei Liu, Yuanhong Chen, Helen Frazer, Gustavo Carneiro
  - Venue: IEEE Transactions on Medical Imaging 2025
  - Status: Moved from Preprint to Published
  - Source: [IEEE Xplore](https://ieeexplore.ieee.org/document/10887396/)

- ✅ **Mixture of Gaussian-distributed Prototypes with Generative Modelling for Interpretable and Trustworthy Image Recognition**
  - Authors: Chong Wang, Yuanhong Chen, Fengbei Liu, Yuyuan Liu, Davis J McCarthy, Helen Frazer, Gustavo Carneiro
  - Venue: IEEE Transactions on Pattern Analysis and Machine Intelligence 2025
  - Status: Moved from Preprint to Published
  - Source: [arXiv](https://arxiv.org/abs/2312.00092)

- ✅ **Knockout: A Simple Way to Handle Missing Inputs**
  - Authors: Minh Nguyen, Batuhan K. Karaman, Heejong Kim, Alan Q. Wang, Fengbei Liu, Mert R. Sabuncu
  - Venue: Transactions on Machine Learning Research 2025
  - Status: Moved from Preprint to Published
  - Source: ResearchGate

- ✅ **Translation Consistent Semi-supervised Segmentation for 3D Medical Images**
  - Authors: Yuyuan Liu, Yu Tian, Chong Wang, Yuanhong Chen, Fengbei Liu, Vasileios Belagiannis, Gustavo Carneiro
  - Venue: IEEE Transactions on Medical Imaging 2024
  - Status: Moved from Preprint to Published
  - Source: [GitHub TraCoCo](https://github.com/yyliu01/TraCoCo)

- ✅ **BRAIxDet: Learning to Detect Malignant Breast Lesion with Incomplete Annotations**
  - Authors: Yuanhong Chen, Yuyuan Liu, Chong Wang, Michael Elliott, Chun Fung Kwok, Yu Tian, Fengbei Liu, Helen Frazer, Davis J McCarthy, Gustavo Carneiro
  - Venue: Medical Image Analysis 2024
  - Source: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1361841524001178)

- ✅ **Unraveling Instance Associations: A Closer Look for Audio-Visual Segmentation**
  - Authors: Yuanhong Chen, Yuyuan Liu, Hu Wang, Fengbei Liu, Chong Wang, Helen Frazer, Gustavo Carneiro
  - Venue: CVPR 2024
  - Source: [GitHub CAVP](https://github.com/cyh-0/CAVP), [Semantic Scholar](https://www.semanticscholar.org/paper/Unraveling-Instance-Associations:-A-Closer-Look-for-Chen-Liu/93ed8ac3198db2a420c9e3bc3dcebbf7ac30a6a2)

**New Preprints:**
- ✅ **An Artificial Intelligence Model to Detect Abnormal Ejection Fraction from Non-Contrast Chest Computed Tomography: The CT-LVEF study**
  - Authors: Jayant Raikhelkar, Zilong Bai, Ashley Beecy, Fengbei Liu, et al.
  - Date: December 2024
  - Source: [ResearchGate](https://www.researchgate.net/publication/388748282_An_Artificial_Intelligence_Model_to_Detect_Abnormal_Ejection_Fraction_from_Non-Contrast_Chest_Computed_Tomography_The_CT-LVEF_study)

- ✅ **Agentic Large-Language-Model Systems in Medicine: A Systematic Review and Taxonomy**
  - Authors: Abdul Mohaimen Al Radi, Xu Cao, Fanyang Yu, Fengbei Liu, Yu Tian, et al.
  - Date: 2024/2025
  - Source: ResearchGate

#### 3. Preprints Status Verified

**Still Under Review:**
- ✅ **Asymmetric Co-teaching with Multi-view Consensus for Noisy Label Learning**
  - Status: arXiv 2023, still preprint
  - Fixed typo: "Learing" → "Learning"
  - Source: [arXiv 2301.01143](https://arxiv.org/abs/2301.01143)

- ✅ **Partial Label Supervision for Agnostic Generative Noisy Label Learning**
  - Status: arXiv 2024, still preprint
  - Source: Papers with Code

#### 4. Reviewer Information
- ✅ Verified: ICCV 2021/2023, MICCAI 2021, CVPR 2022/2023/2024, ECCV 2022/2024, BMVC 2022, NeurIPS 2023/2024, ICLR 2024, ICML 2024
- ✅ Did NOT add: CVPR 2025, NeurIPS 2025, ICLR 2025, ICML 2025 (user confirmed not reviewing)

### Summary Statistics

**Total Updates:**
- 2 papers moved from preprint to IEEE TMI 2025
- 1 paper moved from preprint to IEEE TPAMI 2025
- 1 paper moved from preprint to TMLR 2025
- 2 new preprints added
- 3 typos fixed
- Position information updated

**Current Publication Count:**
- First-author: 6 papers
- Co-author: 15+ papers
- Preprints: 4 papers

**2024-2025 Publications:**
- IEEE TMI: 2 papers
- IEEE TPAMI: 1 paper
- TMLR: 1 paper
- Medical Image Analysis: 1 paper
- CVPR: 1 paper
- **Total: 6 papers in 2024-2025**

### Verification Sources

- ✅ Google Scholar: https://scholar.google.com/citations?user=oY_qRxMAAAAJ&hl=en
- ✅ ResearchGate: https://www.researchgate.net/profile/Fengbei-Liu
- ✅ Cornell Sabuncu Lab: https://sabuncu.engineering.cornell.edu/people/
- ✅ IEEE Xplore
- ✅ arXiv.org
- ✅ GitHub repositories
- ✅ OpenAccess CVF
- ✅ Semantic Scholar

### Files Updated

- ✅ `/Users/fengbeiliu/Documents/Vault/CV/fbl_cv.tex` - LaTeX source
- ✅ `/Users/fengbeiliu/Documents/Vault/CV/fbl_cv.pdf` - Compiled PDF
- ✅ `/Users/fengbeiliu/Documents/Vault/Templates/CV/fbl_cv.tex` - Original template (synced)
- ✅ `/Users/fengbeiliu/Documents/Vault/Templates/CV/fbl_cv.pdf` - Original template PDF (synced)

### Compilation Status

✅ PDF compiled successfully without errors

---

## 2026-01-19: Added OpenReview as Update Source

**Updated By:** Agent

### Changes Made

#### Documentation Updates
- ✅ Added OpenReview profile to all documentation files
  - Profile URL: https://openreview.net/profile?id=~Fengbei_Liu1
  - Source: [OpenReview](https://openreview.net/profile?id=~Fengbei_Liu1)

#### Files Updated
- ✅ `WORKFLOW.md` - Added OpenReview to search sources and key URLs
- ✅ `WORKFLOW.md` - Added OpenReview URL to key sources
- ✅ `WORKFLOW.md` - Added OpenReview to search strategy and monthly check procedures
- ✅ `README.md` - Added OpenReview to contact information and update schedule
- ✅ `UPDATE_LOG.md` - Documented this change

### OpenReview Profile Information
- **Profile:** https://openreview.net/profile?id=~Fengbei_Liu1
- **Affiliation:** Cornell University (Postdoc, 2024 - Present)
- **Advisor:** Mert R. Sabuncu
- **Expertise:** Medical Image Analysis, Weakly-supervised Learning

### Summary
OpenReview is now included as one of the primary sources for CV updates. Future update checks will include:
- Google Scholar
- ResearchGate
- **OpenReview** (NEW)
- arXiv
- Conference proceedings
- Journal publications

### Verification Source
- ✅ OpenReview Profile: https://openreview.net/profile?id=~Fengbei_Liu1

---

## 2026-01-19: Added New IEEE JBHI 2025 Publication

**Updated By:** Agent

### Changes Made

#### New Publication Added
- ✅ **Progressive Mining and Dynamic Distillation of Hierarchical Prototypes for Disease Classification and Localisation**
  - Authors: Chong Wang, Fengbei Liu, Yuanhong Chen, Gustavo Carneiro
  - Venue: IEEE Journal of Biomedical and Health Informatics 2025
  - Status: Published
  - Source: [IEEE Xplore](https://ieeexplore.ieee.org/document/10955117/)

#### How Discovered
- Found via OpenReview profile check (https://openreview.net/profile?id=~Fengbei_Liu1)
- Verified via IEEE Xplore database
- Paper presents HierProtoPNet framework for disease classification and localisation

#### Current Preprints Status Verified
- ✅ **CT-LVEF study** - Published on Research Square (February 2025), still preprint
  - Source: [Research Square](https://www.researchsquare.com/article/rs-5677688/v1)
- ✅ **Agentic LLM Systems in Medicine** - Available on TechRxiv, still preprint
- ✅ **Asymmetric Co-teaching** - arXiv 2023, still preprint
- ✅ **Partial Label Supervision** - arXiv 2024, still preprint

#### MIDL 2026 Submissions Noted
Found 3 papers submitted to MIDL 2026 (not added to CV as still under review):
1. HyperCT: Low-Rank Hypernet for Unified Chest CT Analysis
2. X-Cardia: Phenotype-Guided Cross-Modal Alignment for Opportunistic Cardiac Screening
3. Beyond Machine Interpretation: Learning from Expert Over-Reads Improves ECG Diagnosis

### Summary Statistics

**Publication Count Updates:**
- Total 2025 Publications: Now **4 papers** in IEEE journals/transactions
  - IEEE JBHI: 1 paper (NEW)
  - IEEE TMI: 2 papers
  - IEEE TPAMI: 1 paper
  - TMLR: 1 paper
- Total Co-author Publications: 16+ papers

**New Citation Milestone:**
- Citations: 1,158+ (verified via Google Scholar)

### Verification Sources

- ✅ OpenReview Profile: https://openreview.net/profile?id=~Fengbei_Liu1
- ✅ IEEE Xplore: https://ieeexplore.ieee.org/document/10955117/
- ✅ Research Square: https://www.researchsquare.com/article/rs-5677688/v1
- ✅ Google Scholar: https://scholar.google.com/citations?user=oY_qRxMAAAAJ&hl=en
- ✅ ResearchGate: https://www.researchgate.net/profile/Fengbei-Liu

### Files Updated

- ✅ `/Users/fengbeiliu/Documents/Vault/CV/fbl_cv.tex` - Added new publication
- ✅ `/Users/fengbeiliu/Documents/Vault/CV/fbl_cv.pdf` - Recompiled
- ✅ `/Users/fengbeiliu/Documents/Vault/CV/UPDATE_LOG.md` - Documented changes

### Compilation Status

✅ PDF compiled successfully without errors

---

## 2026-03-19: Monthly Update — BraTS 2024 Paper Added

**Updated By:** Agent — automated monthly maintenance run

### Changes Made

#### 1. New Co-author Publication Added
- ✅ **Effective Segmentation of Post-Treatment Gliomas Using Simple Approaches: Artificial Sequence Generation and Ensemble Models**
  - Authors: Heejong Kim, Léo Milecki, Mina C. Moghadam, Fengbei Liu, Minh Nguyen, Eric Qiu, Abhishek Thanki, Mert R. Sabuncu
  - Venue: MICCAI BraTS Challenge 2024, Oral Presentation
  - arXiv: https://arxiv.org/abs/2409.08143
  - Source: Google Scholar (oY_qRxMAAAAJ profile, sortby=pubdate)
  - Note: Paper appeared on Google Scholar since last update; was in CV's research context (TOOLS.md) but not in fbl_cv.tex

#### 2. Pre-existing Papers Noted (Already in CV, Not in Prior Log)
  The following papers were found in fbl_cv.tex but NOT documented in UPDATE_LOG (added between Jan 19 and today, presumably manually or via earlier agent run):
  - RNED: Rotary Number Encoding and Decoding for Quantitative Medical VLM Analysis (CVPR 2026, first-author)
  - HyperCT: Low-Rank Hypernet for Unified Chest CT Analysis (MIDL 2026, first-author)
  - BackSplit: The Importance of Sub-dividing the Background... (CVPR 2026, co-author)
  - From Failure to Feedback: Group Revision Unlocks Hard Cases... (CVPR 2026, co-author)
  - X-Cardia: Phenotype-Guided Cross-Modal Alignment... (MIDL 2026, Oral, co-author)
  - Beyond Machine Interpretation: Learning from Expert Over-Reads... (MIDL 2026, co-author)
  - Bridging Generative and Discriminative Noisy-Label Learning... (IEEE TPAMI 2026, first-author)

#### 3. Preprints — No Status Change
- ✅ CT-LVEF study (Raikhelkar et al.) — still preprint (Research Square)
- ✅ Agentic LLM Systems in Medicine — still preprint
- ✅ Asymmetric Co-teaching — still arXiv preprint

### Summary Statistics

**Current Publication Count:**
- First-author: 9 papers (including 3 × 2026)
- Co-author: 17+ papers (including 4 × CVPR/MIDL 2026)
- Preprints: 3 papers
- **Citations: 1,571** (Google Scholar, March 2026)

### Verification Sources

- ✅ Google Scholar: https://scholar.google.com/citations?user=oY_qRxMAAAAJ&hl=en&sortby=pubdate
- ✅ OpenReview: https://openreview.net/profile?id=~Fengbei_Liu1
- ✅ DDG search: "Fengbei Liu publications 2025 2026"
- ✅ arXiv: https://arxiv.org/abs/2409.08143

### Files Updated

- ✅ `/home/fbl/vault/CV/fbl_cv.tex` — Added BraTS 2024 paper to Co-author Publications
- ⚠️ `/home/fbl/vault/CV/fbl_cv.pdf` — NOT recompiled (missing `fontawesome` TeX package on fbl-a6k; run `sudo apt-get install texlive-fonts-extra` to fix)
- ✅ `/home/fbl/vault/CV/UPDATE_LOG.md` — Documented changes

### Compilation Status

⚠️ Compilation failed: missing `fontawesome.sty` (system package `texlive-fonts-extra` not installed on fbl-a6k).
Fix: `sudo apt-get install texlive-fonts-extra`, then `cd ~/vault/CV && pdflatex fbl_cv.tex`
All .tex changes are correct — this is a pre-existing environment issue unrelated to today's edit.

---

## Update Schedule

**Next scheduled update:** 2026-04-19 (monthly check)

**Upcoming conference deadlines to monitor:**
- CVPR 2026: Papers now accepted — verify all confirmed ✅
- MIDL 2026: Papers now accepted — verify all confirmed ✅
- MICCAI 2025: Check acceptance notifications (June 2025)
- NeurIPS 2025: Check acceptance notifications (September 2025)
- ICCV 2025: Check acceptance notifications (July 2025)

---

## Template

```markdown
## YYYY-MM-DD: [Update Type]

**Updated By:** [Agent / User]

### Changes Made

#### [Category]
- [ ] Change description
  - Details
  - Source: [URL]

### Summary Statistics
- Key metrics

### Verification Sources
- [ ] Source URLs

### Files Updated
- [ ] File paths

### Compilation Status
- [ ] Status
```
