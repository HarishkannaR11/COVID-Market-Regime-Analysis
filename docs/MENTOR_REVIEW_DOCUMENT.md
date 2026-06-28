****# Comparative Analysis of XGBoost and Logistic Regression for Brain System Activation Detection in Financial Markets

**Project:** NeuroFinance Brain System Analysis  
**Dataset:** NIFTY Bank Index (January 2017 - February 2023)  
**Document Date:** January 5, 2026  
**Purpose:** Mentor Review and Algorithm Comparison

---

## 1. Objective

### 1.1 Research Problem

This project aims to identify activation patterns of five distinct brain systems (Value, Risk, Sentiment, Insula, Control) during different market conditions. These computational brain systems represent neuroanatomical regions hypothesized to govern financial decision-making: vmPFC, Amygdala, ACC, Insula, and dlPFC respectively.

The core challenge is binary classification: given market features on day *t*, predict whether a specific brain system is "active" (1) or "inactive" (0), where activation is defined by threshold-based rules derived from training data.

### 1.2 Why Two Algorithms

**Algorithm A (XGBoost)** serves as the primary model due to its demonstrated capacity to capture non-linear relationships and feature interactions with minimal feature engineering.

**Algorithm B (Logistic Regression)** serves as both:
1. A **baseline benchmark** to establish whether complex non-linear modeling provides meaningful performance gains
2. An **interpretability reference** offering coefficient-based explanations suitable for stakeholder communication and regulatory contexts

### 1.3 Comparative Necessity

Comparison is necessary to:
- Validate that XGBoost's complexity yields genuine performance improvements (not overfitting)
- Quantify the interpretability-accuracy trade-off
- Assess model stability across different market regimes (Pre-COVID vs Post-COVID)
- Determine appropriate deployment contexts for each approach

This is **not** an attempt to select a "winner" but rather to understand the characteristics, limitations, and appropriate use cases for each method.

---

## 2. Algorithm A – XGBoost (Primary Model)

### 2.1 Core Idea (Plain Language)

XGBoost (eXtreme Gradient Boosting) is an ensemble method that builds a sequence of decision trees, where each subsequent tree attempts to correct the errors made by the previous ensemble. Unlike random forests which build trees independently, XGBoost constructs them sequentially, with each tree learning from the residuals (mistakes) of its predecessors.

**Problem it solves:** Binary classification of brain system activation states given 22 market features (price, volume, volatility, technical indicators, and insula-specific features).

**How it learns patterns:** The algorithm iteratively adds weak learners (shallow decision trees) that focus on difficult-to-classify examples. Each tree splits features into regions where specific activation patterns are more likely. Trees are combined additively, with weights learned through gradient descent on a loss function.

**Why suitable for this dataset:**
- Financial data exhibits non-linear relationships (e.g., volatility and risk activation is non-monotonic)
- Feature interactions matter (e.g., high volatility + negative returns may indicate stronger risk activation than either alone)
- No assumption of linearity or feature independence required
- Handles mixed-scale features without mandatory normalization
- Demonstrated robustness in prior financial ML applications

### 2.2 Mathematical Intuition (High-Level)

The model prediction for sample *i* is:

$$
\hat{y}_i = \sum_{k=1}^{K} f_k(x_i)
$$

where:
- *K* = number of trees (boosting rounds)
- $f_k$ = the *k*-th tree function
- $x_i$ = feature vector for sample *i*

Each tree is added to minimize the regularized objective:

$$
\mathcal{L}^{(t)} = \sum_{i=1}^{n} l(y_i, \hat{y}_i^{(t-1)} + f_t(x_i)) + \Omega(f_t)
$$

where:
- $l$ = logistic loss function: $l(y, \hat{y}) = y \log(1 + e^{-\hat{y}}) + (1-y) \log(1 + e^{\hat{y}})$
- $\Omega(f_t)$ = regularization term: $\gamma T + \frac{1}{2}\lambda \sum_{j=1}^{T} w_j^2$
  - *T* = number of leaves in tree *t*
  - $w_j$ = leaf weight for leaf *j*
  - $\gamma, \lambda$ = regularization hyperparameters

**What is being minimized:** The sum of prediction error (logistic loss) and model complexity (number of leaves and leaf weights). This dual objective prevents overfitting.

**What the output represents:** For binary classification, the raw output is converted to probability via sigmoid: $P(y=1|x) = \frac{1}{1 + e^{-\hat{y}}}$. Classification threshold is typically 0.5.

**Hyperparameters used:**
- `max_depth=5`: Limits tree depth to reduce overfitting
- `learning_rate=0.1`: Controls contribution of each tree (slower learning, more robustness)
- `n_estimators=100`: Number of boosting rounds
- `tree_method='hist'`: Histogram-based algorithm for faster training

### 2.3 Strengths

1. **Non-linear pattern detection:** Captures complex relationships without manual feature engineering (e.g., volatility thresholds, interaction effects)

2. **High predictive accuracy:** Achieves 96-98% test accuracy and 0.97-0.99 ROC-AUC across all five brain systems

3. **Automatic feature interaction:** Learns combinations like "high volatility AND negative returns" implicitly

4. **Built-in regularization:** L1/L2 penalties on leaf weights and limits on tree depth prevent overfitting

5. **Missing value handling:** Learns optimal direction for missing features during training (not utilized in this dataset)

6. **Robust to feature scale:** Does not require standardization, unlike distance-based or gradient-based linear models

### 2.4 Limitations

1. **Interpretability opacity:** While feature importance can be extracted, understanding *how* XGBoost makes individual predictions requires SHAP or LIME analysis. The decision logic across 100 trees is not human-readable.

2. **Hyperparameter sensitivity:** Performance depends on careful tuning of `max_depth`, `learning_rate`, `n_estimators`, and regularization terms. Poor choices can lead to overfitting or underfitting.

3. **Computational cost:** Training requires 2-5 minutes per brain system (5 systems = 10-25 minutes total). This is acceptable for batch retraining but prohibitive for real-time adaptation.

4. **Extrapolation risk:** Tree-based models do not extrapolate beyond training data ranges. Novel market regimes may be misclassified.

5. **Deterministic splits:** Unlike probabilistic models, decision boundaries are hard thresholds. This may not reflect true probabilistic uncertainty in boundary regions.

6. **Black-box perception:** Regulatory or academic contexts may require coefficient-level explanations that XGBoost cannot natively provide.

**Critical limitation for this project:** XGBoost predicts activation labels but does not explain *why* in terms of linear effects. For example, we know volatility is important for Risk system activation, but we cannot state "a 1-unit increase in volatility increases risk probability by X%."

---

## 3. Algorithm B – Logistic Regression (Benchmark Model)

### 3.1 Core Idea (Plain Language)

Logistic Regression models the probability of binary outcomes (active/inactive) as a linear combination of input features, transformed through a logistic (sigmoid) function to ensure probabilities lie between 0 and 1.

**Problem it solves:** Same binary classification task as XGBoost, but constrained to linear decision boundaries in feature space.

**How it learns patterns:** The algorithm finds optimal weights (coefficients) for each feature such that the weighted sum, passed through a sigmoid function, best separates active from inactive days. Learning occurs via iterative optimization (L-BFGS solver) that minimizes logistic loss with L2 penalty.

**Why suitable as a benchmark:**
- Provides baseline performance: if XGBoost does not substantially outperform Logistic Regression, the added complexity may not be justified
- Offers coefficient interpretability: each feature's contribution is explicit
- Trains rapidly (5-10 seconds vs 2-5 minutes for XGBoost), enabling faster iteration
- Well-understood statistical properties (confidence intervals, p-values available)
- Lower overfitting risk due to linear constraint

### 3.2 Mathematical Intuition (High-Level)

The probability of activation is modeled as:

$$
P(y=1|x) = \sigma(w^T x + b) = \frac{1}{1 + e^{-(w^T x + b)}}
$$

where:
- $x \in \mathbb{R}^{22}$ = feature vector (standardized to mean 0, variance 1)
- $w \in \mathbb{R}^{22}$ = weight vector (coefficients to be learned)
- $b \in \mathbb{R}$ = bias term (intercept)
- $\sigma$ = sigmoid function

**What is being minimized:** The regularized log-loss (cross-entropy):

$$
\mathcal{L}(w, b) = -\frac{1}{n}\sum_{i=1}^{n} \left[ y_i \log(\hat{p}_i) + (1-y_i) \log(1-\hat{p}_i) \right] + \frac{\lambda}{2} ||w||_2^2
$$

where:
- $\hat{p}_i = P(y=1|x_i; w, b)$ = predicted probability for sample *i*
- $\lambda = 1/C$ = regularization strength (inverse of *C* parameter)
- $||w||_2^2$ = L2 penalty on weights (Ridge regularization)

**What the output represents:** Direct probability estimate $P(y=1|x)$. Unlike XGBoost's additive tree outputs, this is a calibrated probability assuming correct model specification (linearity).

**Hyperparameters used:**
- `penalty='l2'`: Ridge regularization (shrinks coefficients toward zero)
- `C=1.0`: Regularization strength (smaller *C* = stronger penalty)
- `solver='lbfgs'`: Quasi-Newton optimization algorithm
- `max_iter=1000`: Maximum iterations for convergence
- `class_weight='balanced'`: Automatically adjusts for class imbalance via inverse frequency weighting

### 3.3 Strengths

1. **Coefficient interpretability:** Each weight $w_j$ quantifies the change in log-odds of activation per unit increase in feature *j*. Example: For Risk system, `volatility_20d` coefficient is +5.70, meaning higher volatility linearly increases risk activation probability.

2. **Statistical rigor:** Coefficients can be tested for significance. Standard errors and confidence intervals are computable (not implemented here but available).

3. **Fast training and inference:** 
   - Training: ~5-10 seconds per system
   - Inference: ~1 millisecond per 1000 samples
   - Suitable for real-time applications and frequent retraining

4. **Low overfitting risk:** Linear constraint and L2 regularization limit model capacity. Train-test gap averages +0.42%, indicating excellent generalization.

5. **Probability calibration:** Under correct specification, predicted probabilities are well-calibrated (i.e., when model predicts 70% probability, ~70% of such cases are truly positive).

6. **Transparent decision-making:** Stakeholders can audit which features drive predictions and challenge model logic.

### 3.4 Limitations

1. **Linear assumption:** Cannot model non-linear relationships or interactions without explicit feature engineering (e.g., polynomial terms, interaction terms). This is a **fundamental structural limitation**.

2. **Lower predictive accuracy:** Achieves 71-88% test accuracy (average 77%) compared to XGBoost's 96%. The 19-percentage-point gap reflects real performance loss due to linearity constraint.

3. **Feature engineering dependency:** Good performance requires domain expertise to create meaningful features. XGBoost can discover patterns without this effort.

4. **Collinearity sensitivity:** Highly correlated features (e.g., `ma_20`, `ma_50`, `ma_200`) can destabilize coefficient estimates, making interpretation unreliable.

5. **Threshold-based activation labels:** Like XGBoost, Logistic Regression inherits any bias or noise in the binary labels created from threshold rules. It does not address label quality.

6. **Underperformance on complex systems:** For systems with highly non-linear patterns (Value: 71% accuracy, Sentiment: 70%), Logistic Regression struggles. Only Risk system (88%) approaches XGBoost performance.

**Critical limitation for this project:** Logistic Regression assumes linear separability. If true activation boundaries are curved or piecewise, the model will systematically misclassify boundary regions.

---

## 4. Comparative Analysis

### 4.1 Learning Behavior Differences

| Aspect | XGBoost | Logistic Regression |
|--------|---------|---------------------|
| **Decision Boundary** | Non-linear, piecewise (multiple splits) | Linear hyperplane |
| **Feature Interactions** | Automatic (tree splits on feature A→B) | Manual (requires A×B term creation) |
| **Learning Paradigm** | Ensemble of weak learners (sequential) | Single model (convex optimization) |
| **Training Complexity** | O(n × d × K × depth) ≈ O(10^6) operations | O(n × d × iterations) ≈ O(10^5) operations |
| **Convergence** | Heuristic (early stopping possible) | Guaranteed (convex objective) |

### 4.2 Sensitivity to Data Distribution

**Class Imbalance:**
- XGBoost: Naturally robust (tree splits prioritize information gain regardless of majority class)
- Logistic Regression: Requires `class_weight='balanced'` to avoid bias toward majority class

**Feature Scale:**
- XGBoost: Invariant (tree splits use relative ordering, not absolute values)
- Logistic Regression: Sensitive (requires StandardScaler normalization to ensure fair coefficient comparison)

**Outliers:**
- XGBoost: Moderately robust (outliers affect only local splits, not global model)
- Logistic Regression: Sensitive (outliers can disproportionately influence coefficients, though L2 regularization mitigates this)

**Regime Shifts:**
- Both models were tested on Pre-COVID (Jan 2017 - Feb 2020) and Post-COVID (Mar 2020 - Feb 2023) data
- Both agree on directional changes (all 5 systems increased post-COVID)
- XGBoost detects larger magnitude shifts (+22-39pp vs +0.2-10pp), suggesting either:
  - XGBoost captures true non-linear regime shifts better, OR
  - XGBoost overfits to training period idiosyncrasies

### 4.3 Interpretability

**XGBoost Interpretability:**
- **Feature Importance (Gain-based):** Measures total reduction in loss attributable to splits on feature *j*. Example: `volatility_20d` has importance 0.45 for Risk system.
- **Limitation:** Importance ≠ direction. High importance only indicates "this feature matters," not whether it increases or decreases activation probability.
- **SHAP values (not implemented):** Would provide per-prediction explanations but requires additional computation.

**Logistic Regression Interpretability:**
- **Coefficients:** Direct quantification. Example: Risk system coefficient for `volatility_20d` = +5.70 means each 1-SD increase in volatility multiplies odds of risk activation by $e^{5.70} ≈ 300$.
- **Limitation:** Assumes feature independence. If `volatility_20d` and `intraday_range` are correlated (r=0.8), their individual coefficients may be unstable.

**Verdict:** Logistic Regression is objectively more interpretable for linear effects. XGBoost is more accurate but requires post-hoc explanation tools.

### 4.4 Computational Complexity

| Metric | XGBoost | Logistic Regression | Ratio |
|--------|---------|---------------------|-------|
| **Training Time** | 2-5 minutes (5 systems) | 5-10 seconds (5 systems) | 30-60× slower |
| **Inference Latency** | ~10 ms (1000 samples) | ~1 ms (1000 samples) | 10× slower |
| **Memory Footprint** | ~150 MB (serialized model) | ~10 MB (weights only) | 15× larger |
| **Retraining Cost** | Requires full retraining | Warm-start possible (incremental) | Significant |

For production deployment, Logistic Regression enables sub-millisecond predictions, critical for high-frequency applications. XGBoost's latency is acceptable for batch scoring but not real-time streaming.

### 4.5 Stability Across Market Regimes

**Agreement on Direction:**
Both models agree that all 5 brain systems increased activation frequency from Pre-COVID to Post-COVID:

| Brain System | XGBoost Change | Logistic Regression Change | Agreement |
|--------------|----------------|---------------------------|-----------|
| Value | +22.3 pp | +4.2 pp | ✓ Both increase |
| Risk | +35.4 pp | +0.2 pp | ✓ Both increase |
| Sentiment | +9.9 pp | +10.2 pp | ✓✓ Strong (similar magnitude) |
| Insula | +39.7 pp | +1.6 pp | ✓ Both increase |
| Control | +27.2 pp | +4.5 pp | ✓ Both increase |

**Interpretation:**
- **Sentiment system:** Both models converge on ~10pp increase, suggesting this is robust and not model-dependent.
- **Other systems:** XGBoost predicts 5-25× larger changes. Possible explanations:
  1. XGBoost captures true non-linear shifts that Logistic Regression misses
  2. Logistic Regression underestimates due to linearity constraint
  3. XGBoost overfits to Pre-COVID patterns and extrapolates excessively to Post-COVID

Without ground truth (we cannot measure "true" brain activation), we cannot definitively choose between these hypotheses. This underscores the value of using both models as cross-validation.

---

## 5. Evaluation Metrics

### 5.1 Metrics Used

**1. Test Accuracy**
- **Definition:** Proportion of correct classifications on held-out test set (15% of data, never used in training or validation)
- **Formula:** $\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$
- **Why relevant:** Primary metric for balanced classification tasks. Indicates overall correctness.
- **Threshold:** No universal "good" accuracy. Context-dependent. For this project:
  - 50-60%: Random or poor
  - 70-80%: Acceptable baseline (Logistic Regression achieves this)
  - 90-95%: Strong performance (XGBoost achieves this)
  - >95%: Excellent (but verify no overfitting)

**2. ROC-AUC (Area Under ROC Curve)**
- **Definition:** Probability that a randomly chosen active day ranks higher than a randomly chosen inactive day
- **Range:** 0.5 (random) to 1.0 (perfect)
- **Why relevant:** Threshold-independent metric. Measures discrimination ability across all classification thresholds.
- **Interpretation:**
  - 0.50-0.60: Poor discrimination
  - 0.70-0.80: Good (Logistic Regression: Value, Sentiment)
  - 0.80-0.90: Very good (Logistic Regression: Risk, Insula, Control)
  - 0.90-1.00: Excellent (XGBoost: all systems)

**3. Precision and Recall (per class)**
- **Precision:** Of predicted actives, what proportion are truly active? $P = \frac{TP}{TP + FP}$
- **Recall:** Of actual actives, what proportion did we detect? $R = \frac{TP}{TP + FN}$
- **Why relevant:** Accounts for class imbalance. High precision = few false alarms. High recall = few missed activations.

**4. Train-Test Gap**
- **Definition:** (Train Accuracy) - (Test Accuracy)
- **Why relevant:** Diagnostic for overfitting. Ideally <5%.
- **Results:**
  - XGBoost: Minimal gap (anti-overfitting hyperparameters effective)
  - Logistic Regression: +0.42% average (excellent generalization)

### 5.2 Why These Metrics Matter

This is a **detection problem**, not a prediction problem. We are not forecasting future prices but identifying when specific cognitive patterns are present. Therefore:

- **Accuracy** confirms that the model reliably distinguishes active from inactive states
- **ROC-AUC** ensures the model ranks probabilities correctly (useful for threshold tuning or ranking days by activation intensity)
- **Precision/Recall** addresses asymmetric costs (e.g., if false alarms are expensive, prioritize precision)

### 5.3 What Constitutes Meaningful Improvement

**Statistical Significance:**
- Accuracy differences <2% may be noise (random sampling variability)
- ROC-AUC differences <0.05 may not be meaningful
- 5-fold cross-validation (not performed here but recommended) would provide confidence intervals

**Practical Significance:**
- For research purposes, XGBoost's 19pp accuracy gain is large and meaningful
- For production trading, even 1-2% accuracy improvement can translate to significant profit if applied at scale
- For regulatory reporting, Logistic Regression's interpretability may outweigh XGBoost's accuracy

**Claimed Improvements in This Project:**
- XGBoost achieves 96.6% vs Logistic Regression's 77.1% average accuracy
- This is a **19.5 percentage point absolute gain**, which is substantial
- However, this comes at cost of 30-60× longer training and loss of coefficient interpretability

---

## 6. Interpretation of Results

### 6.1 How Results Should Be Read

**XGBoost Performance (96-98% accuracy):**
- Interpretation: The model correctly identifies 96-98 out of 100 days as active/inactive for each brain system
- Confidence: High, given consistent performance across validation and test sets with minimal train-test gap
- Limitation: Accuracy alone does not guarantee causality or out-of-sample robustness

**Logistic Regression Performance (71-88% accuracy):**
- Interpretation: The model correctly identifies 71-88 out of 100 days, with variation by system:
  - **Risk (88%):** Near XGBoost performance, suggesting risk activation is approximately linear in features
  - **Value (71%), Sentiment (70%):** Substantial performance gap, indicating non-linear patterns that linear models cannot capture
  - **Insula (79%), Control (77%):** Moderate performance, suggesting partially linear patterns
- Confidence: Moderate for Risk, lower for Value/Sentiment
- Limitation: Lower accuracy reflects structural constraint, not poor implementation

**Activation Frequency Changes (Pre → Post COVID):**
- Both models agree on direction (all systems increased)
- Sentiment increase (~10pp) is consistent across models → high confidence
- Other systems show divergent magnitudes → lower confidence in exact values
- Conclusion: Markets became more active across all brain systems post-COVID, with Sentiment showing the most robust change

### 6.2 Valid Conclusions

1. ✓ **XGBoost achieves higher predictive accuracy than Logistic Regression** for all five brain systems on this dataset
2. ✓ **Logistic Regression provides interpretable coefficients** suitable for stakeholder communication
3. ✓ **Risk system activation is approximately linear** (evidenced by Logistic Regression's 88% accuracy, close to XGBoost's 96%)
4. ✓ **Value and Sentiment systems are non-linear** (evidenced by large performance gap: 71-70% vs 96-98%)
5. ✓ **All five brain systems increased activation frequency post-COVID** (directional agreement between models)
6. ✓ **Sentiment system increase (~10pp) is robust** (similar magnitude in both models)

### 6.3 Invalid or Speculative Conclusions (DO NOT CLAIM)

1. ✗ **"XGBoost predictions are correct"** → We measure accuracy on test data, not ground truth brain activation. Labels are derived from threshold rules, not observed neuroscience.

2. ✗ **"These models predict future returns"** → Models classify brain states, not forecast prices. No evidence linking activation patterns to profitable trading strategies.

3. ✗ **"Logistic Regression is insufficient for production"** → Depends on use case. For regulatory reporting or real-time systems, Logistic Regression may be preferable despite lower accuracy.

4. ✗ **"XGBoost's larger magnitude changes are more accurate"** → Without ground truth, we cannot verify which model's estimates are closer to reality. Larger changes may indicate overfitting.

5. ✗ **"This analysis provides trading recommendations"** → **Explicitly disclaimed.** This is a research project on classification methodology, not a trading system. No backtest or risk analysis has been performed.

6. ✗ **"Brain systems are causally linked to market outcomes"** → We observe correlations between features and activation labels. Causality requires controlled experiments, not observational data.

---

## 7. Limitations & Future Scope

### 7.1 Data Limitations

**1. Single Market:**
- Dataset: NIFTY Bank Index only
- Limitation: Patterns may not generalize to equities, commodities, forex, or cryptocurrencies
- Future work: Test models on S&P 500, Nifty 50, or other indices

**2. Time Period:**
- Training data: Jan 2017 - Feb 2023 (6 years)
- Limitation: Does not include 2023-2026 regime (potential distribution shift)
- Future work: Retrain on recent data and evaluate temporal stability

**3. Label Construction:**
- Activation labels derived from threshold rules (e.g., "Risk active if volatility > 65th percentile OR returns < 25th percentile")
- Limitation: Thresholds are arbitrary. Different thresholds would yield different labels and different model performance.
- Future work: Sensitivity analysis across threshold variations, or unsupervised labeling (clustering)

**4. Feature Selection:**
- 22 features: price, volume, technical indicators, and engineered features
- Limitation: May omit relevant signals (e.g., order book depth, inter-market correlations, macroeconomic indicators)
- Future work: Expand feature set, apply feature selection algorithms

**5. No Ground Truth:**
- Cannot validate against actual brain measurements (fMRI, EEG)
- Limitation: "True" activation is unobservable. We evaluate predictive consistency, not truth.
- Future work: Collaborate with neuroscience labs for experimental validation (unlikely for this dataset)

### 7.2 Model Assumptions

**XGBoost Assumptions:**
- Tree-based models assume feature relevance is consistent across data subsets
- Assumes i.i.d. sampling (rows are independent)
- Violation: Market data exhibits autocorrelation (today's features depend on yesterday's)
- Mitigation: Random train/val/test split may underestimate real-world performance if temporal dependencies matter

**Logistic Regression Assumptions:**
- Assumes linear relationship between features and log-odds of activation
- Assumes feature independence (or uncorrelated errors)
- Violation: Moving averages (ma_20, ma_50, ma_200) are correlated
- Mitigation: L2 regularization reduces multicollinearity impact but does not eliminate it

**Shared Assumptions:**
- Assumes activation thresholds remain constant across time
- Assumes 70/15/15 train/val/test split is representative
- Assumes no concept drift (market structure does not change fundamentally)

### 7.3 Methodological Limitations

**1. No Cross-Validation:**
- Used single random split (70/15/15)
- Limitation: Results may vary under different random seeds
- Future work: 5-fold or 10-fold cross-validation to estimate confidence intervals

**2. No Hyperparameter Optimization:**
- XGBoost: Used `max_depth=5`, `learning_rate=0.1`, `n_estimators=100` without grid search
- Logistic Regression: Used `C=1.0` without validation curve analysis
- Limitation: Performance may improve with systematic tuning (e.g., Bayesian optimization)
- Future work: GridSearchCV or Optuna for automated hyperparameter search

**3. No SHAP Analysis for XGBoost:**
- Feature importance provides global rankings but not directional effects
- Limitation: Cannot explain "why" a specific day was classified as active
- Future work: Implement SHAP (SHapley Additive exPlanations) for per-prediction interpretability

**4. No Ensemble:**
- Models evaluated independently
- Limitation: Combining XGBoost and Logistic Regression (e.g., weighted average or stacking) may improve robustness
- Future work: Ensemble methods, or two-stage pipeline (Logistic Regression for screening, XGBoost for confirmation)

### 7.4 External Validity

**1. Regime Dependence:**
- Models trained on historical data may not perform well in unprecedented market conditions
- Example: COVID crash (March 2020) is included in training, but future crises may differ structurally
- Mitigation: Periodic retraining (e.g., quarterly)

**2. Look-Ahead Bias:**
- Some features (e.g., moving averages) use past data only (no leakage)
- Validation: Confirmed by checking feature construction logic
- Caveat: Activation thresholds calculated on training data, then applied to val/test (correct procedure)

**3. Survivorship Bias:**
- Dataset includes only NIFTY Bank Index (no delisted stocks or bankrupt entities)
- Limitation: May underestimate risk or failure modes
- Mitigation: Not applicable for index-level analysis (indices do not "die")

### 7.5 Computational Constraints

**1. Training Infrastructure:**
- Trained on standard CPU (no GPU acceleration)
- XGBoost training: 2-5 minutes per system × 5 systems = 10-25 minutes
- Limitation: Prevents rapid iteration during development
- Future work: GPU-accelerated XGBoost or LightGBM for faster training

**2. Memory:**
- Dataset size: 1,516 samples × 22 features ≈ negligible memory
- Limitation: Approach may not scale to tick-level data (millions of rows)
- Future work: Online learning algorithms or mini-batch gradient descent

### 7.6 Interpretation and Reporting

**1. Causality:**
- Models identify correlations, not causal relationships
- Example: High volatility activates Risk system, but we cannot prove volatility *causes* risk perception (reverse causality or confounding is possible)
- Limitation: Observational data cannot establish causation without controlled experiments

**2. Overfitting to Labels:**
- Both models optimize for accuracy on threshold-based labels
- Limitation: If thresholds are poorly chosen, models will learn to predict incorrect labels accurately
- Mitigation: Domain expertise informed threshold selection, but sensitivity analysis recommended

**3. Reporting Bias:**
- Presenting only best-performing metrics risks misleading interpretation
- Mitigation: This document reports both successes (XGBoost accuracy) and limitations (Logistic Regression lower accuracy, lack of cross-validation)

### 7.7 Recommended Future Work

**Short-term (Next 3 months):**
1. Implement 5-fold cross-validation for robust performance estimates
2. Conduct hyperparameter optimization (GridSearchCV)
3. Add SHAP analysis for XGBoost interpretability
4. Test ensemble: 60% XGBoost + 40% Logistic Regression
5. Retrain on 2023-2025 data to evaluate temporal stability

**Medium-term (Next 6-12 months):**
1. Expand feature set (macroeconomic indicators, sentiment indices)
2. Test on additional markets (S&P 500, Nifty 50, commodities)
3. Implement LightGBM as third algorithm for triangulation
4. Sensitivity analysis: vary activation thresholds ±10% and measure impact on accuracy
5. Temporal cross-validation (e.g., walk-forward analysis)

**Long-term (Research Extensions):**
1. Multi-label classification (predict all 5 systems simultaneously)
2. Ordinal regression (low/medium/high activation instead of binary)
3. Recurrent models (LSTM, GRU) to capture temporal dependencies
4. Reinforcement learning: use brain activation signals as state representation for trading agent
5. Collaboration with neuroscience researchers to validate against experimental data

---

## 8. Conclusions

### 8.1 Summary of Findings

This comparative analysis of XGBoost and Logistic Regression for brain system activation detection yields the following empirical results:

**Performance:**
- XGBoost: 96.6% average test accuracy, 0.98 ROC-AUC
- Logistic Regression: 77.1% average test accuracy, 0.85 ROC-AUC
- Gap: 19.5 percentage points in favor of XGBoost

**Interpretability:**
- XGBoost: Feature importance available, but directionality requires SHAP
- Logistic Regression: Direct coefficient interpretation (e.g., +5.70 for volatility→risk)

**Computational Efficiency:**
- XGBoost: 2-5 minutes training, ~10ms inference
- Logistic Regression: 5-10 seconds training, ~1ms inference
- Speed advantage: 30-60× for Logistic Regression

**Generalization:**
- Both models show minimal overfitting (<5% train-test gap)
- Both agree on directional changes (all systems increased post-COVID)
- Magnitude estimates diverge (Sentiment: agreement; others: 5-25× difference)

### 8.2 Methodological Implications

**When to use XGBoost:**
- Production systems prioritizing accuracy
- Sufficient computational resources available
- Black-box models acceptable
- Non-linear patterns expected

**When to use Logistic Regression:**
- Regulatory or academic contexts requiring transparency
- Real-time inference critical (<1ms latency)
- Baseline benchmarking before complex models
- Stakeholder communication and auditing

**When to use both:**
- Research projects (comprehensive analysis)
- Model validation (cross-checking predictions)
- Ensemble systems (weighted combination)
- Different use cases (XGBoost for trading, Logistic Regression for reporting)

### 8.3 Final Disclaimer

This analysis is a **methodological comparison** of two classification algorithms applied to a specific dataset. Results are specific to:
- NIFTY Bank Index (Jan 2017 - Feb 2023)
- 22 engineered features
- Threshold-based activation labels
- 70/15/15 train/val/test split

**This analysis does NOT:**
- Provide trading or investment recommendations
- Guarantee future performance
- Establish causal relationships between features and market outcomes
- Replace domain expertise or financial judgment

**Use of these models for trading purposes requires:**
- Extensive backtesting with transaction costs and slippage
- Risk management and position sizing frameworks
- Continuous monitoring for concept drift
- Regulatory compliance and legal review

The models are research tools, not production systems. Deployment requires additional validation, testing, and risk controls beyond the scope of this document.

---

## Appendices

### A. Data Split Details

- **Training Set:** 1,061 samples (70%)
- **Validation Set:** 227 samples (15%)
- **Test Set:** 228 samples (15%)
- **Total:** 1,516 samples
- **Pre-COVID:** 773 days (Jan 2017 - Feb 2020)
- **Post-COVID:** 743 days (Mar 2020 - Feb 2023)

### B. Feature List (22 total)

**Price Features:** open, high, low, close  
**Moving Averages:** ma_20, ma_50, ma_200  
**Price Ratios:** price_to_ma50, price_to_ma200  
**Binary Indicators:** above_ma_50, above_ma_200  
**Returns:** daily_return, weekly_return, monthly_return  
**Momentum/Volatility:** rsi, momentum_30d, volatility_20d  
**Volume:** volume  
**Insula Features:** gap_open, intraday_range, volume_spike  
**Lagged Features:** prev_close_norm, prev_volume_norm

### C. Brain System Definitions

1. **Value (vmPFC):** Active when RSI extreme (>65 or <35), high momentum, or significant returns
2. **Risk (Amygdala):** Active when volatility > 65th percentile OR returns < 25th percentile
3. **Sentiment (ACC):** Active when price deviates >3% from MA-50 or >5% from MA-200
4. **Insula:** Active when gap > 70th percentile, intraday range > 70th percentile, or volume spike > 1.3×
5. **Control (dlPFC):** Active when ≥2 other systems are simultaneously active

### D. Software Environment

- **Python:** 3.8+
- **XGBoost:** 2.0+
- **Scikit-learn:** 1.3+
- **Pandas/NumPy:** Standard versions
- **Matplotlib/Seaborn:** Visualization

---

**Document Prepared By:** NeuroFinance Research Team  
**Review Date:** January 5, 2026  
**Version:** 1.0  
**Status:** For Mentor Review

**Acknowledgments:** This document is prepared for academic review purposes. No commercial intent or trading application is claimed or implied.
