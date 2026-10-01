<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=KPI%20%26%20Success%20Metrics&fontSize=28&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf%20v4%20%C2%B7%20Production%20Validation&descAlignY=78&descSize=15)

</div>

This document tracks **verified build-time engineering KPIs** against baseline targets, and outlines **operational service-level metrics** for production deployment.

<br/>

## 1. Verified Build-Time Engineering KPIs

All metrics below are computed from executable code against our hand-verified **180-listing holdout Gold Standard set** (`data/gold_labeling_sheet.csv`) and production cross-validation:

| Metric Category | Target Baseline | v4 Production Actual | Verified Artifact / Code | Status |
|---|:---:|:---:|---|:---:|
| **Weak Supervision Cohen's $\kappa$** | > 0.35 | **0.5890** (+131% gain) | `src/labeling/evaluate_labels.py` | ✅ |
| **Weak Supervision Gold F1** | > 0.50 | **0.7130** (+57% gain) | `data/gold_evaluation_results.csv` | ✅ |
| **GroupKFold Out-of-Fold AUC** | > 0.80 | **0.9961** (Unseen Employers) | `data/model_benchmark_group_cv.csv` | ✅ |
| **Holdout Gold Test ROC-AUC** | > 0.80 | **0.9200** (Calibrated RF) | `data/model_benchmark_gold_test.csv` | ✅ |
| **Holdout Gold Test F1 Score** | > 0.60 | **0.7080** (GBM) / **0.6949** (RF) | `data/model_benchmark_gold_test.csv` | ✅ |
| **Holdout Gold Ghost Recall** | > 0.75 | **0.9318** (RF) / **1.0000** (Agent) | `data/agent_benchmark_results.csv` | ✅ |
| **Platt Calibrated Brier Score** | < 0.025 | **0.0167** (+11.2% gain) | `data/calibration_metrics_v4.csv` | ✅ |
| **Expected Calibration Error (ECE)** | < 0.050 | **0.0220** (-40% error) | `data/calibration_metrics_v4.csv` | ✅ |
| **Survival Half-Life Ratio** | > 2.0x | **42.6x** (128.0d vs 3.0d) | `data/survival_summary_metrics.csv` | ✅ |
| **Description Plagiarism Rate** | > 20% | **54.47%** (1,553 postings) | `data/cross_company_plagiarism.csv` | ✅ |
| **FastAPI Real-Time Latency** | < 50ms | **< 15ms** | `src/api/main.py` | ✅ |
| **Pytest Quality Gate Pass Rate** | 100% | **100% (11 / 11 tests passed)** | `tests/` | ✅ |
| **SQL Forensic Queries** | ≥ 25 | **42 queries across 9 categories** | `02_SQL/naukri_saaf_sql_workbench.sql` | ✅ |

<br/>

## 2. Operational Service-Level Metrics (Production Plan)

| Metric | Business Value | Measurement Mechanism | SLA / Threshold |
|---|---|---|---|
| **API Availability & Uptime** | Service reliability for extension and aggregators | `/health` endpoint probe | $\ge 99.9\%$ uptime |
| **Population Stability Index (PSI)** | Early detection of portal hiring and salary shifts | `src/monitoring/drift_detector.py` | $\text{PSI} < 0.25$ (Alert if $\ge 0.25$) |
| **Data Quality Gate** | Prevents malformed scrapes from corrupting pipeline | `src/monitoring/data_validation.py` | 0 SchemaErrors allowed |
| **Client-Side Privacy Guarantee** | Guarantees zero resume leakage | Local in-browser PDF.js tokenization | 0 external network transmissions |
| **Agent Forensic Audit Speed** | Reduces human recruiter verification time | `src/agent/verifier.py` (4 tools) | $< 5.0\text{s}$ per listing audit |

<br/>

## 3. Continuous Improvement Backlog

| Priority | Enhancement | Target Milestone | Business Impact |
|:---:|---|:---:|---|
| **P1** | Automated Daily Apify Ingestion Cron | v4.1 | Continuous freshness and automated drift alerts |
| **P2** | In-Extension Opt-In Feedback ("Was this listing active?") | v4.2 | Real-time human feedback loop for active retraining |
| **P3** | Direct ATS Webhook Integration (Greenhouse, Lever) | v4.3 | Cross-verification against private company hiring feeds |
| **P4** | Multi-Language Scrape Parsing (French, German, Hindi) | v4.4 | Expansion to EMEA and APAC regional recruitment portals |
