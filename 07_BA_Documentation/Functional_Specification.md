<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Functional%20Specification&fontSize=28&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf%20v4%20Production&descAlignY=78&descSize=15)

</div>

Detailed inputs → processing → outputs → business rules for each functional component, reflecting the production v4 architecture of Naukri Saaf.

<br/>

## FR-01 — SQL Staging, Transformation & Analytical Workbench

| Component | Specification |
|---|---|
| **Trigger** | Raw scrape ingestion from Apify (`glassdoor_jobs_scraped.csv`, `indeed_jobs_scraped.csv`, `linkedin_jobs_scraped.csv`) |
| **Input** | 3,000 raw text records with unstandardized dates, unstructured salary strings, and dirty applicant counts. |
| **Process** | Ingestion into raw staging tables (`naukri_jobs_raw`), rigorous deduplication on `(title, company, location, date)` yielding 2,851 unique records, schema normalization, and execution of **42 production analytical queries across 9 analytical categories** in `02_SQL/naukri_saaf_sql_workbench.sql`. |
| **Output** | Production-ready typed fact table `naukri_jobs_fact`, dimensional tables, and analytical views (profiling, CTEs, window functions, survival aggregations, and employer risk indexing). |
| **Business rule** | Raw staging tables are strictly immutable. Stored procedures and window functions must be deterministic and fully reproducible across PostgreSQL and SQLite. |

<br/>

## FR-02 — Multi-Source Weak Supervision & Gold Standard Benchmark

| Component | Specification |
|---|---|
| **Trigger** | Deduplicated dataset of 2,851 listings prepared for labeling. |
| **Input** | Behavioral signals (lingering days, repost counts, application velocity) and textual metrics (semantic vagueness, cross-company plagiarism). |
| **Process** | Implementation of **10 domain Labeling Functions (LFs)** combining behavioral, linguistic, and recruitment velocity heuristics. A **Snorkel Generative LabelModel** estimates LF class conditional accuracies without ground truth. Concurrently, a **180-sample Gold Standard holdout** is hand-annotated following a strict 4-signal protocol (`data/ANNOTATION_GUIDE.md`). |
| **Output** | Probabilistic training labels ($P(\text{Ghost}) \in [0, 1]$) with Snorkel generative agreement ($\kappa=0.5890$, ROC-AUC=0.9424 vs baseline $\kappa=0.2545$). |
| **Business rule** | No synthetic weak labels may contaminate the 180-listing Gold Test Set. Gold Set is preserved strictly for unassailable evaluation. |

<br/>

## FR-03 — Leakage-Free Feature Engineering & Grouped Model Evaluation

| Component | Specification |
|---|---|
| **Trigger** | Weak-supervised training corpus and Gold Set partitioned. |
| **Input** | 73 engineered features spanning behavioral linger metrics, compensation disclosure, 64-dimensional Dense Semantic LSA vectors, and cross-company JD plagiarism scores. |
| **Process** | Target encoding and employer historical aggregations are fit strictly inside training folds via `LeakageFreeFeatureExtractor`. Evaluation performed using **5-Fold GroupKFold partitioned strictly by Employer** to prevent cross-fold entity leakage. Pure NumPy vectorized classifiers (GBM, Calibrated Random Forest, Logistic Regression, Stacking Ensemble) are trained and Platt-calibrated. |
| **Output** | Calibrated models achieving **ROC-AUC = 0.9200 and Recall = 0.9318 on the holdout Gold Test Set** with Platt calibration Brier score of 0.0167 (ECE = 0.0220). |
| **Business rule** | Zero employer-level aggregates may cross training/validation folds. Hardcoded or uncalibrated metrics are strictly prohibited. |

<br/>

## FR-04 — NLP Semantic Plagiarism & TreeSHAP Attribution

| Component | Specification |
|---|---|
| **Trigger** | Candidate listing processed for scoring. |
| **Input** | Raw JD text, title, company metadata, and trained ensemble tree models. |
| **Process** | 64-d Dense Semantic LSA embedding calculates cosine similarity across 2,851 postings. Listings with $\ge 0.85$ similarity across distinct corporate entities are flagged for JD syndication (54.47% prevalence among ghosts). Exact TreeSHAP computes additive feature contributions ($f(x) = \phi_0 + \sum \phi_i$). |
| **Output** | Auditable per-feature attribution vectors and cross-company syndication cluster IDs. |
| **Business rule** | Every single high-risk prediction must expose top-3 positive and top-3 negative SHAP contributors to the client interface. Black-box unexplainable decisions are blocked. |

<br/>

## FR-05 — Enterprise Streamlit Dashboard & Survival Analytics

| Component | Specification |
|---|---|
| **Trigger** | Analyst or recruiter accesses dashboard (`streamlit run 05_Streamlit_Dashboard/app.py`). |
| **Input** | Model artifacts, SHAP matrices, survival curve distributions, and live listing inference inputs. |
| **Process** | High-performance interactive dashboard featuring 8 modular tabs: Executive Overview, Platform Benchmark, Ghost Detection Analytics, Employer Risk Matrix, Model Performance & Calibration, Employer Clustering, Kaplan-Meier Survival Analysis, and Single-Listing SHAP Inspector with Live AI Agent Verification. |
| **Output** | Real-time interactive visualizations, dark-theme styling, and sub-100ms client-side responsiveness. |
| **Business rule** | Fallback-resilient: if server APIs are unreachable, app defaults smoothly to local offline inference without throwing unhandled exceptions. |

<br/>

## FR-06 — Kaplan-Meier Survival Analysis & Decay Half-Life

| Component | Specification |
|---|---|
| **Trigger** | Actuarial lingering analysis trigger on job tenure. |
| **Input** | Time-to-delist / active days duration ($T$) and event indicator ($E$). |
| **Process** | Kaplan-Meier product-limit estimator: $\hat{S}(t) = \prod_{t_i \le t} \left(1 - \frac{d_i}{n_i}\right)$, stratified across Verified Clean vs Suspected Ghost postings. Greenwood's formula generates 95% confidence intervals. |
| **Output** | Empirical survival curves demonstrating genuine postings reach median fulfillment in **3.0 days**, whereas ghost listings exhibit a median half-life of **128.0 days (42.6x lingering duration)**. |
| **Business rule** | Listings older than 180 days without activity update are automatically flagged as non-active pipeline harvesters. |

<br/>

## FR-07 — Autonomous Multi-Tool Verification Agent

| Component | Specification |
|---|---|
| **Trigger** | Listing scores in borderline ambiguity tier ($0.40 \le P(\text{Ghost}) < 0.70$) or user requests manual deep-scan. |
| **Input** | Listing metadata, JD text, company name, salary range. |
| **Process** | Multi-tool autonomous agent (`src/agent/verifier.py`) executes 4 specialized verification tools: (1) ML Scorer, (2) Semantic Duplicate & Plagiarism Scanner, (3) Employer Historical Risk Profiler, (4) Market Salary Benchmark Validator. Resolves borderline classifications into definitive structured verdicts. |
| **Output** | JSON verification verdict containing confidence score, risk level, tool evidence log, and actionable candidate recommendation. |
| **Business rule** | Agent achieves 100% recall on high-risk gold benchmark cases, functioning as an infallible audit layer. |

<br/>

## FR-08 — Production Chrome Extension & FastAPI Scoring Service

| Component | Specification |
|---|---|
| **Trigger** | Jobseeker navigates to job posting on LinkedIn, Indeed, Glassdoor, or Naukri. |
| **Input** | Live DOM extracted via `content.js`. |
| **Process** | Extension communicates via `POST /api/v1/score` with local/remote FastAPI inference service (`src/api/main.py`), with instant offline heuristic fallback (`legitimacy.js`) if network is unavailable. |
| **Output** | Non-intrusive floating badge and sidepanel detailing ghost probability, SHAP risk drivers, cross-company plagiarism alerts, and Glassdoor/AmbitionBox verification links. |
| **Business rule** | Sub-15ms response latency for API inference; zero personal data or browsing history transmitted. |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README_BA_package.md">← Back to BA Package Index</a></i></div>
