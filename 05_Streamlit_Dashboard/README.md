# 05 — Streamlit Analytics Command Center

## 🚀 Interactive Web Application

The **Naukri Saaf Streamlit Command Center** is a multi-tab web application for investigating job posting authenticity, model calibration metrics, employer risk profiles, and live scoring.

---

## 💻 Launching the Application

From the root project directory:
```bash
streamlit run 05_Streamlit_Dashboard/app.py
```
The application will launch automatically in your browser at `http://localhost:8501`.

---

## 📑 Feature Modules & Tabs

1. **Executive Overview**: High-level KPI metrics cards, overall ghost rate (15.0%), and risk distribution donuts.
2. **Platform Comparison**: Head-to-head transparency and lifespan metrics across Glassdoor, Indeed, and LinkedIn.
3. **Ghost Job Forensics**: Drill-down filters on ghost, suspect, and genuine listings with interactive search.
4. **Employer Risk Matrix**: Top hiring entities ranked by listing velocity, ghost ratios, and market risk exposure.
5. **Model Diagnostics & SHAP**: Feature importance rankings, TreeSHAP force plots, and Platt calibration curves.
6. **K-Means Market Clustering**: Unsupervised cluster profiles grouping postings by text verbosity and compensation signals.
7. **Searchable Data Explorer**: Full CSV filter and export table for deep-dive investigation.

---

## 📖 In-Depth Dashboard Guide

For detailed explanations of all UI components, filters, metric formulas, and troubleshooting steps:
👉 **[DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md)**
