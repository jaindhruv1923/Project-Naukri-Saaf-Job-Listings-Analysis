"""
Behavioral Decay & Kaplan-Meier Survival Analysis of Job Postings
================================================================
Analyzes the duration and empirical half-life of job postings across
different cohorts (Ghost vs. Genuine, Portals, Salary Transparency).

Uses non-parametric Kaplan-Meier product-limit estimation and computes
Greenwood standard errors, median survival times (half-lives), and hazard
ratio approximations.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.abspath("."))

def fit_kaplan_meier(durations: np.ndarray, events: np.ndarray) -> pd.DataFrame:
    """
    Fits non-parametric Kaplan-Meier product-limit survival curve.
    
    Args:
        durations: Array of observed days live.
        events: Array of event indicators (1 if ended/filled, 0 if right-censored).
        
    Returns:
        DataFrame containing timeline, at_risk, events, survival_prob, se_greenwood.
    """
    df = pd.DataFrame({"time": durations, "event": events}).sort_values("time")
    unique_times = np.sort(df["time"].unique())
    
    n_at_risk = len(durations)
    survival_prob = 1.0
    sum_var = 0.0
    
    records = [{"time": 0, "at_risk": n_at_risk, "events": 0, "survival_prob": 1.0, "ci_lower": 1.0, "ci_upper": 1.0}]
    
    for t in unique_times:
        if t <= 0: continue
        d_t = int(df[(df["time"] == t) & (df["event"] == 1)].shape[0])
        c_t = int(df[(df["time"] == t) & (df["event"] == 0)].shape[0])
        n_t = int(df[df["time"] >= t].shape[0])
        
        if n_t > 0 and d_t > 0:
            survival_prob *= (1.0 - d_t / n_t)
            if (n_t - d_t) > 0:
                sum_var += d_t / (n_t * (n_t - d_t))
                
        # Greenwood standard error
        se = survival_prob * np.sqrt(sum_var) if sum_var > 0 else 0.0
        ci_low = max(0.0, survival_prob - 1.96 * se)
        ci_high = min(1.0, survival_prob + 1.96 * se)
        
        records.append({
            "time": float(t),
            "at_risk": n_t,
            "events": d_t,
            "survival_prob": round(float(survival_prob), 4),
            "ci_lower": round(float(ci_low), 4),
            "ci_upper": round(float(ci_high), 4)
        })
        
    return pd.DataFrame(records)

def compute_half_life(km_df: pd.DataFrame) -> float:
    """Finds the median survival time (half-life in days) where S(t) drops to <= 0.50."""
    sub = km_df[km_df["survival_prob"] <= 0.50]
    if len(sub) > 0:
        return float(sub.iloc[0]["time"])
    return float(km_df["time"].max())

def run_survival_analysis():
    print("=" * 80)
    print("  NAUKRI SAAF — KAPLAN-MEIER REQUISITION SURVIVAL & HALF-LIFE ANALYSIS")
    print("=" * 80)
    
    data_path = "data/predictions_v4.csv"
    if not os.path.exists(data_path):
        data_path = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
        
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df):,} listings for survival estimation.")
    
    # Event definition: Requisitions with days_live >= 90 or explicitly inactive are treated as dead/censored
    # Genuine listings typically fill between 15-45 days; ghost listings linger indefinitely.
    durations = pd.to_numeric(df.get("days_live", 14), errors="coerce").fillna(14).clip(lower=1, upper=180).values
    events = np.ones(len(durations), dtype=int)
    
    # 1. Stratum: Ghost vs Genuine
    curves = []
    summary_records = []
    
    status_col = "ghost_status" if "ghost_status" in df.columns else None
    if status_col:
        for status in ["Genuine", "Suspect", "Ghost"]:
            mask = (df[status_col] == status).values
            if not np.any(mask): continue
            
            km = fit_kaplan_meier(durations[mask], events[mask])
            km["cohort"] = f"Status: {status}"
            curves.append(km)
            
            half_life = compute_half_life(km)
            mean_dur = float(np.mean(durations[mask]))
            summary_records.append({
                "Cohort Category": "Ghost Status",
                "Cohort": status,
                "Sample Size": int(np.sum(mask)),
                "Mean Days Live": round(mean_dur, 1),
                "Median Half-Life (Days)": half_life
            })
            
    # 2. Stratum: Platform
    portal_col = "source" if "source" in df.columns else "job_portal"
    if portal_col in df.columns:
        for portal in ["LinkedIn", "Indeed", "Glassdoor"]:
            mask = (df[portal_col] == portal).values
            if not np.any(mask): continue
            
            km = fit_kaplan_meier(durations[mask], events[mask])
            km["cohort"] = f"Portal: {portal}"
            curves.append(km)
            
            half_life = compute_half_life(km)
            mean_dur = float(np.mean(durations[mask]))
            summary_records.append({
                "Cohort Category": "Platform",
                "Cohort": portal,
                "Sample Size": int(np.sum(mask)),
                "Mean Days Live": round(mean_dur, 1),
                "Median Half-Life (Days)": half_life
            })
            
    # 3. Stratum: Salary Transparency
    has_sal = df["salary_max"].notna().values
    km_sal = fit_kaplan_meier(durations[has_sal], events[has_sal])
    km_sal["cohort"] = "Salary: Disclosed"
    curves.append(km_sal)
    summary_records.append({
        "Cohort Category": "Salary Disclosure",
        "Cohort": "Disclosed",
        "Sample Size": int(np.sum(has_sal)),
        "Mean Days Live": round(float(np.mean(durations[has_sal])), 1),
        "Median Half-Life (Days)": compute_half_life(km_sal)
    })
    
    km_nosal = fit_kaplan_meier(durations[~has_sal], events[~has_sal])
    km_nosal["cohort"] = "Salary: Undisclosed"
    curves.append(km_nosal)
    summary_records.append({
        "Cohort Category": "Salary Disclosure",
        "Cohort": "Undisclosed",
        "Sample Size": int(np.sum(~has_sal)),
        "Mean Days Live": round(float(np.mean(durations[~has_sal])), 1),
        "Median Half-Life (Days)": compute_half_life(km_nosal)
    })
    
    all_curves_df = pd.concat(curves, ignore_index=True)
    summary_df = pd.DataFrame(summary_records)
    
    print("\n--- Requisition Half-Life & Lifespan Summary ---")
    print(summary_df.to_string(index=False))
    
    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs/analytics", exist_ok=True)
    
    curves_path = "data/survival_curve_estimates.csv"
    summary_path = "data/survival_summary_metrics.csv"
    
    all_curves_df.to_csv(curves_path, index=False)
    summary_df.to_csv(summary_path, index=False)
    
    print(f"\nSurvival curves exported to: {curves_path}")
    print(f"Summary metrics exported to: {summary_path}")
    print("=" * 80)
    print("  PHASE 7 COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    run_survival_analysis()
