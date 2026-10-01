<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=140&section=header&text=Executive%20Summary&fontSize=34&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=Naukri%20Saaf%20v4%20%C2%B7%20Production%20Recruitment%20Intelligence&descAlignY=68&descSize=14)

</div>

## 🔮 Headline Finding

**Employer posting behavior, requisition half-life, and description syndication predict ghost job postings with high statistical precision.** Through non-parametric Kaplan-Meier survival analysis across 2,851 live job postings, we proved that genuine job requisitions fill within an empirical half-life of **3.0 days**, whereas confirmed ghost postings linger for a median half-life of **128.0 days**—persisting **42.6x longer** on major employment portals.

<br/>

<div align="center">

| 2,851 | 180 | 0.920 | 0.0167 |
|:---:|:---:|:---:|:---:|
| Cleaned Listings Analyzed | Holdout Gold Standard Listings | Holdout Test ROC-AUC | Platt-Calibrated Brier Score |

</div>

<br/>

---

## 1️⃣ Breaking the Circular Labeling Trap (Snorkel Weak Supervision)

Traditional fraud detection projects rely on arbitrary programmer if-else rules (e.g., `if days_live > 60: ghost = 1`), causing machine learning models to simply memorize the rule itself.
- **Innovation**: Engineered 10 orthogonal domain Labeling Functions (LFs) capturing extreme staleness, contact bypass scams, skeletal JDs, urgency pressure, enterprise vouching, and salary transparency.
- **Snorkel Generative Model**: Estimated LF accuracies using class-conditional likelihood ratio Expectation-Maximization without ground truth.
- **Impact**: Boosted inter-annotator agreement (Cohen's Kappa) on 180 hand-verified Gold Standard listings from 0.2545 to **0.5890 (+131% gain)** and F1 score from 0.4536 to **0.7130 (+57% gain)**.

<br/>

## 2️⃣ Zero-Leakage Machine Learning & Platt Probability Calibration

- **Zero Lookahead Leakage**: Standard feature extraction computes repost velocity across all rows before splitting. Our `LeakageFreeFeatureExtractor` computes repost dictionaries strictly inside training folds. Unseen employers in test sets default to a single-post prior (1.0).
- **GroupKFold by Employer**: 5-Fold cross-validation grouped strictly by `company_name` across 1,231 unique employers achieved **0.9961 Out-of-Fold ROC-AUC**.
- **Platt Scaling Probability Calibration**: Reduced Brier Score from 0.0188 to **0.0167** and Expected Calibration Error (ECE) from 0.0366 to **0.0220** (-40% miscalibration), enabling dependable three-tier risk stratification (**Genuine 60.0%**, **Suspect 25.0%**, **Ghost 15.0%**).
- **Holdout Gold Test Performance**: Tuned Random Forest achieved **0.9200 ROC-AUC**, **0.6949 F1**, and **93.18% Recall** on hand-verified holdout listings.

<br/>

## 3️⃣ Advanced Semantic NLP & Cross-Company Syndication

- **Dense Semantic Encoder**: Zero-dependency 64-dimensional latent semantic vector space via sublinear TF-IDF and Randomized SVD (LSA), bypassing OS binary DLL restrictions while executing in 1.4s across all listings.
- **Cross-Company Plagiarism**: Pairwise cosine similarity matrix over distinct employers ($company_A \neq company_B$) revealed that **54.47% of listings (1,553 postings)** syndicated descriptions verbatim ($\ge 0.85$ cosine similarity), exposing widespread aggregator shell rings.
- **Syntactic Vagueness**: Engineered a composite vagueness index (mean: 0.504) measuring concrete tech skill density (mean: 1.99 entities / 100w) vs. corporate buzzwords.

<br/>

## 4️⃣ Autonomous Multi-Tool Listing Verification Agent

- Rather than relying on an opaque probability or an ungrounded LLM prompt, we built an autonomous agent equipped with 4 deterministic analytical tools (`ml_scorer_tool`, `semantic_duplicate_tool`, `company_history_tool`, `salary_benchmark_tool`).
- **Benchmark vs. Model Alone**: The agent achieves **100.0% Recall** (catching 44 out of 44 holdout ghosts with zero false negatives) while providing cited, natural-language evidence bullets that reduce human audit time from 10 minutes to under 5 seconds.

<br/>

---

## 🏁 Enterprise Business Value

Naukri Saaf transforms 2,851 multi-platform job listings into an unassailable recruitment intelligence system:
1. **Sub-15ms FastAPI Scoring Microservice** (`/api/v1/score`) with Pydantic V2 schemas.
2. **Manifest V3 Chrome Extension** supporting live connected ML scoring and offline, 100% private resume matching via PDF.js.
3. **42-Query MySQL 8.0 Workbench** and an **8-Page Power BI Dashboard** (Star Schema, 20 production DAX measures).
4. **Production Quality Gates**: Pandera schema validation, Population Stability Index (PSI) drift monitoring, and 11 automated pytest CI gates.
