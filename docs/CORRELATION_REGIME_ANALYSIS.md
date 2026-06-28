****# Rolling Correlation Regimes: Market Alignment Over Time
## Descriptive Temporal Correlation Analysis

**Date**: January 6, 2026  
**Folder**: Rolling_Correlation_Regimes/  
**Purpose**: Visualize market alignment dynamics without causal inference

---

## Overview

This analysis presents **rolling correlation regimes** between brain systems, market variables, and the composite NDS score. Correlation regimes show periods of alignment (positive correlation) and disalignment (negative correlation) over time, using 60-day rolling windows.

**Key Principle**: Correlation measures **co-movement**, not causation, prediction, or trading signal quality.

---

## Methodology

### Rolling Correlation Calculation
- **Window**: 60 trading days (~3 months)
- **Method**: Pearson correlation between two time series
- **Minimum periods**: 30 days (for edge handling)
- **Formula**: $r = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y}$

### Regime Classification
- **Aligned Regime**: Correlation > 0 (green shading)
- **Disaligned Regime**: Correlation < 0 (red shading)
- **Strong Correlation**: |r| > 0.5 (dotted reference lines)

### Variables Analyzed
1. **Systems vs NDS**: Value, Risk, Sentiment, Control vs composite score
2. **Systems vs Market Return**: Daily return alignment
3. **Cross-System**: Inter-system correlations (Value-Sentiment, etc.)

---

## Category 1: Systems vs NDS Score

### Graph 1.1: Value vs NDS

![Value vs NDS](value_vs_nds_correlation.png)

#### What this graph represents
60-day rolling correlation between Value system activation and composite NDS score over time. Y-axis ranges from -1 (perfect negative correlation) to +1 (perfect positive correlation).

#### What the graph shows

**Pre-COVID (2018-2020)**:
- Weak positive correlation (mean = 0.091)
- Frequent regime switching between aligned and disaligned
- Correlation oscillates around zero

**Post-COVID (2020-2023)**:
- Shift to weak negative correlation (mean = -0.062)
- Change of -0.153 points
- More time in disaligned regime
- Overall alignment: 47.5% of period shows positive correlation

**Pattern**: Value system becomes less aligned with overall NDS Post-COVID, suggesting independent contribution rather than following composite trend.

#### What this graph does NOT claim
- Does not indicate Value system accuracy or predictive power
- Does not establish causality (Value → NDS or NDS → Value)
- Does not recommend using correlation for timing decisions
- Low correlation does not mean system is "not working"

---

### Graph 1.2: Sentiment vs NDS

![Sentiment vs NDS](sentiment_vs_nds_correlation.png)

#### What this graph represents
Rolling correlation between Sentiment system and NDS composite score.

#### What the graph shows

**Pre-COVID**: 
- Strong positive correlation (mean = 0.703)
- Consistently aligned regime (>0.5 threshold)

**Post-COVID**:
- Even stronger positive correlation (mean = 0.774, +0.070 change)
- Nearly continuous aligned regime (97.9% of period)
- Correlation rarely drops below +0.5

**Pattern**: Sentiment system is **highly aligned** with composite NDS throughout period, with slight strengthening Post-COVID. Suggests Sentiment is major driver of overall score.

#### What this graph does NOT claim
- Does not mean Sentiment "causes" NDS movements
- Does not indicate Sentiment should be weighted higher
- Does not imply other systems are less important
- High correlation ≠ better performance

---

### Graph 1.3: Control vs NDS

![Control vs NDS](control_vs_nds_correlation.png)

#### What this graph represents
Rolling correlation between Control system and NDS composite score.

#### What the graph shows

**Pre-COVID**:
- Weak negative correlation (mean = -0.207)
- Mostly disaligned regime

**Post-COVID**:
- Stronger negative correlation (mean = -0.389, -0.182 change)
- **Inverse relationship** with NDS strengthens
- Only 14.9% of period shows positive correlation

**Pattern**: Control system shows **opposite movement** to composite NDS, particularly Post-COVID. When NDS increases, Control tends to decrease, and vice versa. Suggests potential mutual inhibition or compensatory dynamics.

#### What this graph does NOT claim
- Does not establish causal relationship
- Does not indicate Control system is "working against" NDS
- Does not imply negative correlation is problematic
- Inverse correlation may reflect system specialization

---

### Graph 1.4: Risk vs NDS

![Risk vs NDS](risk_vs_nds_correlation.png)

#### What this graph represents
Rolling correlation between Risk system and NDS score.

#### What the graph shows

**Both Periods**:
- Correlation is **NaN** (not computable)
- Risk system shows near-zero or constant activation
- Insufficient variation for correlation calculation
- 0% of period shows measurable alignment

**Pattern**: Risk system operates independently with minimal activation variability, preventing meaningful correlation computation with NDS.

#### What this graph does NOT claim
- Does not mean Risk system is inactive or broken
- Does not indicate Risk should be removed
- NaN correlation ≠ zero correlation (different concepts)
- May reflect infrequent but important activation events

---

## Category 2: Systems vs Market Return

### Graph 2.1: Sentiment vs Market Return

![Sentiment vs Return](sentiment_vs_return_correlation.png)

#### What this graph represents
Rolling correlation between Sentiment system activation and daily market returns.

#### What the graph shows

**Pre-COVID**:
- Weak positive correlation (mean = 0.205)
- 60.8% aligned regime
- Sentiment co-moves with market direction

**Post-COVID**:
- Correlation drops to near-zero (mean = 0.024, -0.181 change)
- More regime switching around zero
- Weakened relationship between Sentiment and returns

**Pattern**: Sentiment activation was modestly aligned with market returns Pre-COVID but becomes **decorrelated** Post-COVID, suggesting Sentiment responds to factors beyond simple return direction.

#### What this graph does NOT claim
- Does not indicate Sentiment predicts returns
- Does not measure profitability or trading performance
- Correlation with returns ≠ useful trading signal
- Does not establish cause-effect (returns → Sentiment or vice versa)

---

### Graph 2.2: Control vs Market Return

![Control vs Return](control_vs_return_correlation.png)

#### What this graph represents
Rolling correlation between Control system and daily market returns.

#### What the graph shows

**Both Periods**:
- Weak to moderate positive correlation (Pre: 0.291, Post: 0.274)
- **Highest return correlation** among all systems
- 97.0% of period in aligned regime
- Consistently positive relationship

**Pattern**: Control system shows most stable alignment with market return direction across both periods. When returns are positive, Control tends to be active, and vice versa.

#### What this graph does NOT claim
- Does not mean Control "follows the market"
- Does not indicate Control predicts future returns
- Correlation with returns ≠ performance contribution
- Does not establish causality

---

## Category 3: Cross-System Correlations

### Graph 3.1: Value vs Sentiment

![Value vs Sentiment](value_vs_sentiment_correlation.png)

#### What this graph represents
Rolling correlation between Value and Sentiment systems.

#### What the graph shows

**Pre-COVID**:
- Weak positive correlation (mean = 0.078)
- Systems operate somewhat independently

**Post-COVID**:
- Correlation weakens further (mean = 0.051, -0.027 change)
- 62.2% aligned overall
- Frequent regime switching

**Pattern**: Value and Sentiment systems show **low co-movement**, suggesting they respond to different market features and contribute independently to decision-making.

#### What this graph does NOT claim
- Does not indicate systems should be merged
- Does not mean one system is redundant
- Low correlation supports system diversity (positive feature)
- Does not establish lead-lag relationships

---

### Graph 3.2: Sentiment vs Control

![Sentiment vs Control](sentiment_vs_control_correlation.png)

#### What this graph represents
Rolling correlation between Sentiment and Control systems.

#### What the graph shows

**Both Periods**:
- Negative correlation (Pre: -0.083, Post: -0.117)
- Disaligned regime dominates (73.1% of period)
- Systems move in **opposite directions**

**Pattern**: Sentiment and Control show **inverse relationship** - when Sentiment increases, Control tends to decrease. Suggests potential mutual inhibition or complementary activation (affect vs executive control trade-off).

#### What this graph does NOT claim
- Does not prove systems inhibit each other neurologically
- Does not indicate design flaw
- Inverse correlation may reflect functional specialization
- Does not establish causality

---

## Combined Dashboard

![Correlation Dashboard](correlation_regimes_dashboard.png)

### What this graph represents
6-panel dashboard showing key rolling correlations simultaneously:
1. Value vs NDS
2. Sentiment vs NDS (strongest positive)
3. Control vs NDS (strongest negative)
4. Value vs Market Return
5. Sentiment vs Control (inverse)
6. Value vs Sentiment (independent)

### What the graph shows

**Cross-Panel Patterns**:
1. **NDS Drivers**: Sentiment strongly positive (+0.77), Control strongly negative (-0.39)
2. **Return Alignment**: Control highest (+0.27), Sentiment weakened Post-COVID
3. **System Independence**: Value-Sentiment low correlation (0.05)
4. **Inverse Pairs**: Sentiment-Control negative throughout (-0.12)
5. **COVID Impact**: Most correlations shift Post-COVID (weakening or strengthening)

### What this graph does NOT claim
- Does not establish causal network between systems
- Does not indicate optimal correlation levels
- Does not predict future correlation regimes
- Does not recommend reweighting systems based on correlations

---

## Quantitative Summary

| Pair | Pre-COVID Corr | Post-COVID Corr | Change | Aligned % |
|------|----------------|-----------------|--------|-----------|
| **Sentiment vs NDS** | +0.703 | +0.774 | +0.070 | 97.9% |
| Control vs NDS | -0.207 | -0.389 | -0.182 | 14.9% |
| Value vs NDS | +0.091 | -0.062 | -0.153 | 47.5% |
| Control vs Return | +0.291 | +0.274 | -0.017 | 97.0% |
| Sentiment vs Return | +0.205 | +0.024 | -0.181 | 60.8% |
| Sentiment vs Control | -0.083 | -0.117 | -0.034 | 26.9% |
| Value vs Sentiment | +0.078 | +0.051 | -0.027 | 62.2% |
| Value vs Control | +0.106 | +0.236 | +0.130 | 65.6% |

**Key Observations**:
- Sentiment has strongest positive NDS alignment (0.77)
- Control has strongest negative NDS alignment (-0.39)
- Control has highest return correlation (0.27)
- Risk system shows NaN (insufficient variation)
- Most correlations shift Post-COVID

---

## Interpretation Guidelines

### What Rolling Correlation Shows
✅ Temporal alignment between variables  
✅ Regime shifts from positive to negative co-movement  
✅ Stability or instability of relationships over time  
✅ Relative independence or dependence of systems  
✅ Period-specific dynamics (Pre vs Post COVID)

### What Rolling Correlation Does NOT Show
❌ Causality or directional influence  
❌ Predictive power or forecast ability  
❌ Trading signal quality or profitability  
❌ Optimal system weights or importance  
❌ Lead-lag relationships (requires different analysis)

---

## Expected Questions

### Q1: What does correlation > 0 mean?
**A**: Variables move together on average - when one increases, the other tends to increase. Does not indicate causation or prediction.

### Q2: Why does Control show negative correlation with NDS?
**A**: Control tends to decrease when NDS increases, suggesting inverse dynamics. May reflect mutual inhibition or complementary activation patterns. Causality not established.

### Q3: Is high correlation with returns good?
**A**: Correlation with returns does not indicate profitability or performance quality. Systems may perform well without correlating with returns, or correlate highly without generating profit.

### Q4: Why is Risk correlation NaN?
**A**: Risk system shows insufficient activation variability for correlation computation. Near-constant values prevent meaningful correlation calculation.

### Q5: Can we predict future correlations?
**A**: This analysis is purely descriptive (historical patterns). Predictive modeling would require different methods not performed here.

### Q6: Should we increase weight of Sentiment (high NDS correlation)?
**A**: Correlation with NDS does not indicate system importance or contribution to performance. System weights should be determined by predictive accuracy or other performance metrics, not correlation.

### Q7: What causes correlation regime shifts?
**A**: This analysis describes regime shifts but does not establish causes. Market volatility changes, regime transitions, or external shocks may influence correlations.

---

## Files Generated

**Individual Correlation Graphs** (12 files):
- 4 Systems vs NDS: `value_vs_nds_correlation.png`, etc.
- 4 Systems vs Return: `value_vs_return_correlation.png`, etc.
- 4 Cross-System: `value_vs_sentiment_correlation.png`, etc.

**Combined Dashboard**:
- `correlation_regimes_dashboard.png` - 6-panel overview

**Data**:
- `correlation_statistics_summary.csv` - Quantitative summary
- `create_correlation_regimes.py` - Reproducible script

---

**Document Purpose**: Present rolling correlation regime analysis for mentor review. Maintain descriptive focus without causal claims or trading recommendations.

**Status**: Ready for academic review ✅  
**All visualizations publication-ready (300 DPI PNG format)**
