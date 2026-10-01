# Naukri Saaf — Machine Learning & Analytics Pipeline (v4 Production)

> **Enterprise Architecture, Mathematical Formulations, and Validation Rigor**  
> *Target Roles: Senior Machine Learning Engineer, Applied Data Scientist, MLOps Engineer*

---

## 1. Executive Summary & Architectural Overview

The **Naukri Saaf ML Subsystem** addresses the systematic market distortion of "Ghost Job Listings"—postings left unfulfilled, duplicated across competing platforms for talent pipeline harvesting, or posted to signal synthetic corporate expansion without active recruitment intent.

In v4, the ML pipeline was re-architected to resolve the critical shortcomings of student/toy ML projects:
1. **Unassailable Ground Truth**: Replaced unverified heuristics with a **180-listing hand-annotated Gold Standard holdout** (`data/gold_labeling_sheet.csv`, `data/ANNOTATION_GUIDE.md`) coupled with **10 domain Labeling Functions (LFs)** modeled via a **Snorkel Generative LabelModel** ($\kappa=0.5890$, ROC-AUC=0.9424).
2. **Zero Leakage & Grouped Cross-Validation**: Replaced naive random train/test splits with **5-Fold GroupKFold partitioned strictly by Employer**. All target encodings and prior probabilities are computed strictly within training folds via `LeakageFreeFeatureExtractor`.
3. **Platt Probability Calibration**: Post-processed raw ensemble tree logits via sigmoid Platt scaling, achieving an institutional Brier score of **0.0167** and Expected Calibration Error (ECE) of **0.0220**.
4. **Dense Semantic NLP & Plagiarism Detection**: Generated 64-dimensional LSA embeddings over 2,851 postings, revealing that **54.47% of ghost listings share plagiarized boilerplate JDs ($\ge 0.85$ cosine similarity)** across competing employers.
5. **Kaplan-Meier Survival Analysis**: Actuarial lingering analysis proving genuine tech openings have a median half-life of **3.0 days**, whereas ghost postings linger **128.0 days (42.6x longer)**.
6. **Additive TreeSHAP Explainability**: Implemented exact tree-path attribution ($f(x) = \phi_0 + \sum_{i=1}^M \phi_i$), guaranteeing local accuracy, consistency, and zero black-box obscurity.

---

## 2. Mathematical Formulations & Component Specifications

### 2.1 Snorkel Generative LabelModel (Weak Supervision)
Given an unlabeled feature vector $x$ and $m=10$ labeling functions $\lambda_1, \dots, \lambda_m \in \{-1, 0, 1\}$, the latent true label $Y \in \{-1, 1\}$ is modeled as:
$$P(Y, \Lambda) = \frac{1}{Z} \exp\left( \theta_0 Y + \sum_{j=1}^m \theta_j Y \Lambda_j + \sum_{j,k} \theta_{jk} \Lambda_j \Lambda_k \right)$$
The parameter vector $\theta$ (representing LF accuracies and propensities) is estimated using the **triplet covariance matrix** without observing true labels $Y$. The resulting marginal posterior $P(Y=1 \mid \Lambda)$ serves as the probabilistic training target.

### 2.2 Platt Sigmoid Probability Calibration
For a raw classifier score $f(x)$, calibrated posterior probability $P(Y=1 \mid f(x))$ is derived via:
$$P(Y=1 \mid f(x)) = \frac{1}{1 + \exp(A \cdot f(x) + B)}$$
Parameters $A$ and $B$ are fit via maximum likelihood on out-of-fold predictions. Calibration quality is measured via the Brier score:
$$\text{BS} = \frac{1}{N} \sum_{i=1}^N (P_i - y_i)^2 = 0.0167$$

### 2.3 Dense Semantic Encoder & Cross-Company Plagiarism
Job descriptions are mapped to a 64-dimensional latent semantic space using Randomized Singular Value Decomposition (LSA):
$$X_{\text{TF-IDF}} \approx U_k \Sigma_k V_k^T \quad (k=64)$$
Pairwise cosine similarity between listing $i$ (Company $A$) and listing $j$ (Company $B \neq A$) is computed:
$$\text{Sim}(i, j) = \frac{u_i \cdot u_j}{\|u_i\| \|u_j\|}$$
Listings with $\text{Sim}(i, j) \ge 0.85$ across different corporate entities are flagged as syndicated boilerplate.

### 2.4 Kaplan-Meier Product-Limit Estimator
The survival function $S(t) = P(T > t)$ estimating the probability of a job posting remaining active beyond $t$ days:
$$\hat{S}(t) = \prod_{t_i \le t} \left(1 - \frac{d_i}{n_i}\right)$$
where $d_i$ is the number of listings delisted at time $t_i$, and $n_i$ is the count of postings active and at risk just prior to $t_i$. Variance is estimated via Greenwood's formula:
$$\widehat{\text{Var}}(\hat{S}(t)) = \hat{S}(t)^2 \sum_{t_i \le t} \frac{d_i}{n_i (n_i - d_i)}$$

---

## 3. Benchmark Results & Verification Table

All metrics below are derived from verified test runs against the **180-Listing Gold Standard Holdout Test Set** (`data/gold_labeling_sheet.csv`):

| Model Architecture | Implementation | Holdout ROC-AUC | Holdout F1-Score | Holdout Recall | Brier Calibration Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Calibrated Random Forest** | NumPy Ensemble | **0.9200** | **0.6721** | **0.9318** | **0.0167** |
| **NumPy Gradient Boosting (GBM)** | Vectorized Trees | **0.9168** | **0.7080** | **0.9091** | **0.0214** |
| **Stacking Meta-Classifier** | Logistic Blending | **0.9150** | **0.6950** | **0.9091** | **0.0189** |
| **NumPy Logistic Regression** | L2 Regularized | **0.8750** | **0.6200** | **0.8636** | **0.0410** |
| *Baseline Weak Heuristic* | Single Cutoff | 0.6200 | 0.4100 | 0.5200 | 0.1850 |

---

## 4. Pipeline Execution & File Inventory

```
03_ML_Pipeline_and_Models/
├── README_ML_PIPELINE.md               # Technical documentation & formulations
├── Naukri_Saaf_ML_Pipeline_v4_PRODUCTION.ipynb # End-to-end production notebook
├── Naukri_Saaf_ML_Pipeline_v3_1_FINAL.ipynb    # Historical v3 baseline reference
├── model_comparison_v3.csv              # Benchmark comparison across models
├── feature_importance_v3.csv           # Tree feature importance weights
├── shap_values_v3.csv                  # Additive TreeSHAP value matrix
├── cluster_profiles_v3.csv             # K-Means employer cluster centroids
└── temporal_cv_results_v3.csv          # Grouped cross-validation logs
```

### Reproducing Pipeline Runs:
```powershell
# 1. Run weak supervision & gold evaluation
python src/models/weak_supervision.py

# 2. Run leakage-free feature extraction & training
python src/models/train_leakage_free_model.py

# 3. Run semantic plagiarism & NLP augmentation
python src/features/dense_semantic_encoder.py

# 4. Run actuarial survival curves
python src/analytics/survival_analysis.py

# 5. Run test suite
pytest -v tests/
```
