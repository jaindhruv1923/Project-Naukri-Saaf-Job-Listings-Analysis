# Naukri Saaf — Resume Bullets & Portfolio Presentation Guide

Use these battle-tested, impact-quantified resume bullet points tailored to your target job applications.

---

## Track 1: Data Analyst / Business Intelligence Analyst

- **Engineered an end-to-end recruitment intelligence pipeline** across 2,851 multi-platform job listings (LinkedIn, Indeed, Glassdoor), deploying MySQL 8.0, Power BI, and Python to identify ghost postings and deceptive hiring practices.
- **Authored 42 production SQL queries** utilizing Recursive CTEs, window functions (`DENSE_RANK()`, `SUM() OVER`), and conditional aggregation to expose that 83.1% of postings concealed salaries, correlating with a **2.4x higher ghost probability**.
- **Architected an 8-page Power BI dashboard** built on a normalized Star Schema with 20 production DAX measures (`CALCULATE`, `KEEPFILTERS`, `SUMX`, `DIVIDE`), analyzing applicant market concentration, regional salary opacity, and requisition decay.
- **Conducted Kaplan-Meier survival analysis** to measure job listing decay, discovering an empirical median half-life disparity of **3.0 days for genuine openings vs. 128.0 days for ghost postings** (persisting 42.6x longer on portals).
- **Developed a dynamic financial & risk workbook in Excel** utilizing `XLOOKUP`, `INDEX-MATCH`, and multi-variable pivot tables with accessible conditional formatting for executive stakeholder reviews.

---

## Track 2: Data Scientist / Machine Learning Engineer

- **Architected a weak supervision framework using Snorkel** (10 domain labeling functions with likelihood ratio Expectation-Maximization) over 2,851 job postings, eliminating circular heuristic labeling and boosting Gold Set Cohen's Kappa from 0.25 to **0.5890** (+131% agreement).
- **Curated a hand-annotated 180-listing holdout Gold Standard benchmark** across LinkedIn, Indeed, and Glassdoor, enforcing strict zero-contamination holdout testing for production model evaluation.
- **Eliminated cross-fold employer lookahead leakage** by building a custom `LeakageFreeFeatureExtractor` with 5-Fold `GroupKFold` cross-validation grouped strictly by company entity across 1,231 unique employers.
- **Engineered pure-vectorized NumPy Gradient Boosting and Tuned Random Forest classifiers**, achieving **0.9200 ROC-AUC, 0.6949 F1, and 0.9318 Recall** on the holdout Gold Set, outperforming the heuristic baseline by **+56% F1**.
- **Implemented Platt Scaling probability calibration**, reducing Brier Score from 0.0188 to **0.0167** (+11.2% improvement) and Expected Calibration Error (ECE) from 0.0366 to **0.0220** (+39.9% error drop).
- **Extracted authentic TreeSHAP decision path attributions**, quantifying global feature drivers (`description_length_words`: 31.4%, `description_lexical_diversity`: 28.7%, `listing_age_bucket`: 10.7%).
- **Built a zero-dependency dense semantic NLP encoder** via sublinear TF-IDF and Randomized SVD (LSA), detecting that **54.5% of listings** syndicated near-verbatim job descriptions across distinct staffing entities ($\ge 0.85$ cosine similarity).

---

## Track 3: AI Engineer / Full-Stack ML Engineer

- **Engineered an Autonomous Listing Verification Agent** orchestrating 4 deterministic Python tools (ML Scorer, Semantic Duplicates, Employer History, Salary Benchmarking) to produce cited forensic audit trails, achieving **100.0% Recall** on holdout test listings.
- **Productionized the model as a sub-15ms FastAPI microservice** with Pydantic V2 schema validation, batch endpoints, and automated CORS handling.
- **Built a dual-mode Manifest V3 Chrome Extension** supporting live connected ML scoring and offline, zero-network private resume matching using PDF.js and client-side tokenizers.
- **Established production quality gates and CI/CD pipelines** using Pandera schema validation, Population Stability Index (PSI) drift monitoring, Docker multi-stage builds, and GitHub Actions CI with 11 automated pytest tests.

---

## Portfolio / LinkedIn Project Summary Blurb

> **Naukri Saaf: Production Multi-Platform Ghost Job Detection & Forensic Analytics Platform**  
> *Technologies: Python, NumPy, Pandas, Scikit-learn, Snorkel, TreeSHAP, FastAPI, Streamlit, MySQL 8.0, Power BI (DAX), Docker, Pandera, Pytest.*  
>  
> Job seekers waste millions of hours applying to "ghost jobs"—postings that companies leave open indefinitely for brand vanity or candidate data collection without active hiring intent. To tackle this, I engineered **Naukri Saaf**, a full-stack data science platform analyzing 2,851 live job postings scraped from LinkedIn, Indeed, and Glassdoor.  
>  
> Rather than relying on naive heuristic rules, I implemented a Snorkel weak supervision generative model over 10 domain labeling functions, evaluated against a hand-annotated 180-listing Gold Standard holdout set. I eliminated target leakage via a custom `LeakageFreeFeatureExtractor` with 5-Fold GroupKFold CV, trained Platt-calibrated tree ensembles achieving 0.9200 ROC-AUC and 93.2% recall, and applied Kaplan-Meier survival analysis to prove that ghost postings persist 42.6x longer than genuine listings (128 days vs. 3 days half-life). To make findings actionable, I built a sub-15ms FastAPI microservice, an interactive Streamlit dashboard, a 42-query MySQL analytics workbench, an 8-page Power BI dashboard, and a Manifest V3 Chrome extension.
