# Neural Decision System Analysis: Results for Mentor Review

**Analysis Method:** XGBoost Brain Activation Model  
**Data Period:** January 2017 – February 2023 (1,516 trading days)  
**Pre-COVID Period:** January 2017 – February 2020 (773 days)  
**Post-COVID Period:** March 2020 – February 2023 (743 days)  
**Systems Analyzed:** Value, Risk, Sentiment, Insula, Control

---

## Results Overview

This document presents descriptive results from XGBoost brain activation analysis comparing cognitive system behavior before and after COVID-19. The analysis examines:

1. **System Activation Regimes** – Binary activation patterns (ON/OFF) for five cognitive systems
2. **Temporal Correlations** – Rolling correlation dynamics between systems and market variables

All results are observational and descriptive. No causal relationships or predictive claims are made.

**Data Source:** Nifty Bank Index data (2017 start) processed through XGBoost classification model generating binary activation states for each cognitive system.

---

## Graphs and Interpretation

### Graph 1: Brain System ON/OFF Regime Dynamics

![ON/OFF Regime Dynamics](all_systems_on_off_regimes.png)

#### What This Graph Represents

This visualization displays the activation regimes of five cognitive systems (Value, Risk, Sentiment, Insula, Control) over time, using a 30-day rolling window to smooth binary activation states. The vertical red line marks the transition from Pre-COVID to Post-COVID period (March 2020).

Each panel shows:
- **Positive values (green/blue/purple)**: System in ON state (active)
- **Negative values (red/orange/yellow)**: System in OFF state (inactive)
- **Rolling window smoothing**: Converts binary 0/1 activations to continuous -1 to +1 scale

#### What The Graph Shows

**Observed Patterns:**

| System | Pre-COVID ON% | Post-COVID ON% | Change |
|--------|---------------|----------------|--------|
| Value | 67.4% | 79.8% | +12.4pp |
| Sentiment | 85.6% | 92.1% | +6.4% |
| Control | 88.2% | 92.6% | +4.4pp |
| Insula | 42.6% | 46.7% | +4.1pp |
| Risk | 40.4% | 45.6% | +5.3pp |

**Key Observations:**
- All five systems show **increased activation** in Post-COVID period
- Sentiment and Control systems maintain **consistently high activation** (>85%) throughout entire period
- Value system shows **largest increase** in activation (+12.4 percentage points)
- Risk and Insula systems remain **near balanced** (40-50% activation) in both periods

#### What This Graph Does NOT Claim

- **No causality**: Does not establish that COVID caused these changes; external factors unexamined
- **No prediction**: Does not forecast future system behavior or market outcomes
- **No trading signal**: Activation patterns are descriptive observations, not actionable recommendations
- **No optimization**: Results reflect observed data characteristics, not optimal strategy performance

---

### Graph 2: Rolling Correlation Regime Dashboard

![Correlation Regimes Dashboard](correlation_regimes_dashboard.png)

#### What This Graph Represents

This 6-panel dashboard displays 60-day rolling Pearson correlations between selected system pairs and market variables. Each panel shows:
- **Green regions**: Aligned regime (positive correlation)
- **Red regions**: Disaligned regime (negative correlation)
- **Black line**: Correlation coefficient over time
- **Gray shaded area**: Post-COVID period

Panels examine correlations between:
1. Value system vs Neural Decision Score (NDS)
2. Sentiment system vs NDS
3. Insula system vs NDS
4. Risk system vs Market Return
5. Risk system vs Sentiment system
6. Sentiment system vs Insula system

#### What The Graph Shows

**Observed Correlation Patterns:**

**System-NDS Relationships:**
- **Value vs NDS**: Strong positive correlation (Pre: 0.70, Post: 0.74), 98% aligned regime
- **Insula vs NDS**: Moderate positive correlation (Pre: 0.57, Post: 0.58), 98% aligned regime
- **Sentiment vs NDS**: Variable alignment, 60% of time in aligned regime

**System-Market Relationships:**
- **Risk vs Market Return**: Consistent negative correlation (-0.38 both periods), only 2% aligned regime
- Risk system shows inverse relationship with daily returns throughout entire period

**Cross-System Relationships:**
- **Risk vs Sentiment**: Predominantly negative correlation (-0.13 Pre, -0.11 Post), 13% aligned regime
- **Sentiment vs Insula**: Weak correlation (0.07 Pre, near-zero Post), 35% aligned regime
- Different cognitive systems show low cross-correlation, suggesting independent activation patterns

**Temporal Stability:**
- Value-NDS and Insula-NDS correlations remain **stable across COVID transition**
- Risk-Market Return correlation shows **no change** between periods
- Most correlations exhibit **temporal consistency** with minor fluctuations

#### What This Graph Does NOT Claim

- **No causality**: Correlations describe co-movement, not cause-effect relationships
- **No directionality**: Does not establish whether systems lead/lag market variables or vice versa
- **No prediction**: Historical correlations do not guarantee future correlation patterns
- **No optimality**: Does not suggest which correlations are desirable or indicate better performance
- **No mechanism**: Does not explain why systems correlate or what drives correlation changes

---

## Expected Questions

### Q1: Why did all systems increase activation post-COVID?

**A:** The observed increase may reflect (a) heightened market volatility triggering more activation conditions, (b) changes in market microstructure post-COVID, or (c) data characteristics in the 2020-2023 period. Causality cannot be established from this descriptive analysis.

### Q2: Why is Risk negatively correlated with market returns?

**A:** The Risk system activates during specific market conditions (likely high volatility or drawdown periods) which tend to coincide with negative daily returns. This is an observed pattern, not a designed feature of the model.

### Q3: Are these results statistically significant?

**A:** Statistical testing was not performed. The results present observed frequencies and correlations across the full dataset (1,516 days). Significance testing would require additional analysis with appropriate null hypotheses.

### Q4: Can these results be used for trading decisions?

**A:** No. This is a descriptive analysis of historical brain activation patterns. The results do not constitute trading advice, performance guarantees, or predictive signals. No backtesting or forward-testing was conducted.

### Q5: What is the Neural Decision Score (NDS)?

**A:** NDS is a weighted combination of the five system activations: `NDS = 0.25×Value + 0.25×Risk + 0.20×Sentiment + 0.15×Insula + 0.15×Control`. The weights are researcher-assigned and not empirically derived.

### Q6: Why are some correlation values showing 'inf' or missing?

**A:** Some systems (Sentiment, Control) have very high activation rates (>85%), resulting in low variance. This can produce numerical instabilities in correlation calculations, especially in rolling window analysis with limited data points.

---

## Summary Statistics

### System Activation Summary (XGBoost Model)

| System | Overall Activation | Pre-COVID | Post-COVID | Period Change |
|--------|-------------------|-----------|------------|---------------|
| Sentiment | 88.8% | 85.6% | 92.1% | +6.4pp |
| Control | 90.4% | 88.2% | 92.6% | +4.4pp |
| Value | 73.5% | 67.4% | 79.8% | +12.4pp |
| Insula | 44.6% | 42.6% | 46.7% | +4.1pp |
| Risk | 42.9% | 40.4% | 45.6% | +5.3pp |

### Key Correlation Findings

| Relationship | Pre-COVID | Post-COVID | Aligned Regime % |
|-------------|-----------|------------|------------------|
| Value ↔ NDS | +0.70 | +0.74 | 98.1% |
| Insula ↔ NDS | +0.57 | +0.58 | 98.1% |
| Risk ↔ Market Return | -0.38 | -0.38 | 1.9% |
| Risk ↔ Sentiment | -0.13 | -0.11 | 13.2% |
| Value ↔ Control | +0.59 | +0.57 | 89.9% |

---

## Technical Notes

**Model Type:** XGBoost binary classification (5 independent classifiers, one per system)  
**Activation Threshold:** Model-determined probability cutoff for binary classification  
**Rolling Window:** 30 days for ON/OFF regime smoothing, 60 days for correlation analysis  
**Period Definition:** Pre-COVID ends February 28, 2020; Post-COVID begins March 1, 2020  
**Data Frequency:** Daily (end-of-day closing prices and features)  

**Analysis Limitations:**
- Descriptive only; no hypothesis testing performed
- Single dataset (Nifty Bank Index); generalizability unknown
- XGBoost hyperparameters and training methodology not detailed in this document
- Missing values in correlation analysis due to low-variance periods not imputed
- Rolling correlations at period boundaries have reduced window sizes

---

## Document Information

**Prepared for:** Mentor Review  
**Analysis Scope:** Descriptive Results Presentation  
**Prepared by:** Research Team  
**Date:** January 2026  
**Data Source:** Nifty Bank Index (2017-2023), XGBoost Brain Activation Model

**Note:** This document presents observational results only. No investment recommendations, causal claims, or predictive statements are made. Further statistical analysis required for inference testing.
