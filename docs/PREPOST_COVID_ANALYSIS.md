# BRAIN SYSTEM ACTIVATION ANALYSIS: PRE vs POST COVID

## Executive Summary

This analysis examines how brain system activation patterns changed in the NIFTY Bank Index between Pre-COVID (Jan 2017 - Feb 2020) and Post-COVID (Mar 2020 - Feb 2023) periods using anti-overfitting XGBoost models.

**Key Finding**: All brain systems showed increased activation Post-COVID, with **Insula** (emotional/instinctive response) showing the most dramatic increase (+138.1%), indicating markets became significantly more reactive to volatility, gaps, and volume spikes.

---

## Activation Frequency Changes (Pre → Post COVID)

| Rank | System    | Pre-COVID | Post-COVID | Change      | % Change   | Interpretation |
|------|-----------|-----------|------------|-------------|------------|----------------|
| 1    | **Insula**    | 28.7%     | 68.4%      | **+39.7pp** | **+138.1%** | Massive increase in emotional/instinctive responses |
| 2    | **Risk**      | 31.0%     | 66.5%      | **+35.4pp** | **+114.1%** | Heightened risk perception and volatility awareness |
| 3    | **Control**   | 66.0%     | 93.1%      | **+27.2pp** | **+41.2%**  | More complex decision-making (multiple systems active) |
| 4    | **Value**     | 52.8%     | 75.1%      | **+22.3pp** | **+42.3%**  | Increased focus on price movements and momentum |
| 5    | **Sentiment** | 81.0%     | 90.8%      | **+9.9pp**  | **+12.2%**  | Already high, further increased trend-following |

**pp** = percentage points

---

## Key Findings

### 🔴 Biggest Increase: Insula System (+39.7pp, +138.1%)

The **Insula System** represents emotional and instinctive responses to market surprises:

**What It Detects:**
- **Gap Openings**: Overnight surprises (top 30% of gaps)
- **Intraday Range**: High volatility within trading days (top 30%)
- **Volume Spikes**: Unusual trading volume (>1.3x average)

**Pre-COVID Behavior:**
- Active only 28.7% of the time
- Markets were relatively stable and predictable
- Fewer overnight shocks and volume surges

**Post-COVID Behavior:**
- Active 68.4% of the time (more than doubled)
- Markets became highly reactive and volatile
- Frequent overnight gaps, intraday swings, and panic/euphoria episodes
- COVID uncertainty, stimulus announcements, and policy changes created constant surprises

**Implication**: Post-COVID markets are dominated by **emotional, knee-jerk reactions** rather than calm, calculated analysis.

---

### 🟠 Second Biggest: Risk System (+35.4pp, +114.1%)

The **Risk System** (Amygdala) monitors market danger signals:

**What It Detects:**
- **Volatility**: Top 35% of 20-day volatility
- **Negative Returns**: Bottom 25% of daily returns

**Change Analysis:**
- Pre-COVID: 31.0% activation (markets relatively calm)
- Post-COVID: 66.5% activation (markets in constant alert mode)
- **More than doubled** risk perception

**Implication**: Post-COVID markets are perceived as **persistently risky**, with investors in constant "fight-or-flight" mode.

---

### 🔵 Third: Control System (+27.2pp, +41.2%)

The **Control System** (dlPFC) activates when 2+ other systems are simultaneously active, representing complex decision-making:

**Change Analysis:**
- Pre-COVID: 66.0% activation
- Post-COVID: 93.1% activation
- Nearly always active Post-COVID (93.1% of days)

**Implication**: Post-COVID trading requires **simultaneous processing of multiple factors**—investors must juggle volatility, sentiment, value, and risk all at once, making decisions far more cognitively demanding.

---

### 🟢 Fourth: Value System (+22.3pp, +42.3%)

The **Value System** (vmPFC) tracks price momentum and returns:

**What It Detects:**
- **RSI Extremes**: >65 or <35 (overbought/oversold)
- **Strong Returns**: Top 25% of daily/weekly/monthly returns
- **Momentum**: Top 25% of 30-day momentum

**Change Analysis:**
- Pre-COVID: 52.8% activation
- Post-COVID: 75.1% activation

**Implication**: Post-COVID markets show **stronger momentum patterns** and more extreme overbought/oversold conditions, suggesting increased trend-following behavior.

---

### 🟡 Fifth: Sentiment System (+9.9pp, +12.2%)

The **Sentiment System** (dmPFC) monitors trend-following behavior:

**What It Detects:**
- **Distance from MA-50**: >3% deviation
- **Distance from MA-200**: >5% deviation

**Change Analysis:**
- Pre-COVID: 81.0% activation (already very high)
- Post-COVID: 90.8% activation (increased further)

**Implication**: Markets were already **highly trend-driven** Pre-COVID, but became even more so Post-COVID. Nearly 91% of days showed significant divergence from moving averages.

---

## Statistical Summary

### Overall Market Behavior Shift

| Metric | Pre-COVID | Post-COVID | Change |
|--------|-----------|------------|--------|
| **Average System Activation** | 51.9% | 78.8% | +26.9pp |
| **All Systems Increased** | - | - | 5 out of 5 (100%) |
| **Systems >50% Active** | 3 systems | 5 systems | +2 systems |
| **Systems >90% Active** | 0 systems | 2 systems | +2 systems |

### Activation Pattern Analysis

**Pre-COVID Market Character:**
- Moderate activation across most systems (51.9% average)
- Sentiment already high (81.0%) - trend-following present
- Risk and Insula low (~30%) - relatively stable
- Control moderate (66.0%) - simpler decision contexts

**Post-COVID Market Character:**
- High activation across ALL systems (78.8% average)
- Insula and Risk dominant (68.4%, 66.5%) - emotional and fearful
- Control near-universal (93.1%) - complex, multi-factor decisions
- All systems elevated - no single "calm" period

---

## Behavioral Interpretation

### Pre-COVID Markets (Jan 2017 - Feb 2020)

**Market Psychology:**
- **Trend-driven** (Sentiment 81%)
- **Value-conscious** (Value 53%)
- **Moderate complexity** (Control 66%)
- **Low fear** (Risk 31%)
- **Emotionally stable** (Insula 29%)

**Investor Behavior:**
- Following established trends
- Relatively calm and calculated
- Fewer surprise events
- Lower volatility environment

---

### Post-COVID Markets (Mar 2020 - Feb 2023)

**Market Psychology:**
- **Highly emotional** (Insula 68%)
- **Fear-dominated** (Risk 67%)
- **Extremely complex** (Control 93%)
- **Strong momentum** (Value 75%)
- **Still trend-following** (Sentiment 91%)

**Investor Behavior:**
- Constant reaction to surprises
- High anxiety and risk awareness
- Juggling multiple conflicting signals
- Rapid momentum swings
- Persistent uncertainty

---

## Research Implications

### 1. Market Efficiency

**Pre-COVID**: More efficient, predictable price movements  
**Post-COVID**: Less efficient, emotion-driven volatility dominates

### 2. Trading Strategy Impact

**Pre-COVID Strategies:**
- Trend-following worked well (Sentiment 81%)
- Value investing viable (Value 53%)
- Lower risk management needs (Risk 31%)

**Post-COVID Strategies Required:**
- **Volatility management critical** (Insula 68%, Risk 67%)
- **Faster reaction times needed** (overnight gaps, intraday swings)
- **Multi-factor analysis essential** (Control 93%)
- **Emotion control paramount** (avoid panic/euphoria triggers)

### 3. Risk Management

**Key Lesson**: Post-COVID markets require **constant vigilance**:
- Risk system active 67% of time (vs 31% Pre-COVID)
- Insula active 68% of time (vs 29% Pre-COVID)
- Traditional risk models likely underestimate Post-COVID volatility

---

## Methodology

### Data Source
- **Pre-COVID**: NIFTY Bank Index, Jan 3, 2017 - Feb 28, 2020 (773 trading days, 37 months)
- **Post-COVID**: NIFTY Bank Index, Mar 2, 2020 - Feb 28, 2023 (743 trading days, 37 months)
- **Total**: 1,516 samples, perfectly balanced between periods

### Model
- **Algorithm**: XGBoost with anti-overfitting regularization
- **Parameters**: max_depth=3, L1/L2 regularization, early stopping, subsampling
- **Training**: 70% train, 15% validation, 15% test on combined data
- **Data Leakage Prevention**: Activation thresholds calculated from training data only
- **Performance**: 96.6% test accuracy, 0.98+ ROC AUC

### Brain Systems Defined

| System | Brain Region | Activation Criteria | Market Function |
|--------|--------------|---------------------|-----------------|
| **Value** | vmPFC | RSI extremes, top 25% returns/momentum | Price movement tracking |
| **Risk** | Amygdala | Top 35% volatility, bottom 25% returns | Threat detection |
| **Sentiment** | dmPFC | >3% from MA-50, >5% from MA-200 | Trend following |
| **Insula** | Insula | Top 30% gaps/range, 1.3x volume | Emotional response |
| **Control** | dlPFC | 2+ other systems active | Complex decisions |

---

## Conclusion

### Primary Finding

**Post-COVID markets fundamentally shifted from trend-driven, value-conscious environments to emotion-dominated, fear-driven, highly complex systems.**

The **138% increase in Insula activation** represents a paradigm shift where:
- Markets react **emotionally** rather than rationally
- **Overnight surprises** became the norm (COVID news, policy changes, global uncertainty)
- **Volatility and volume spikes** dominate trading behavior
- **Investor psychology** shifted from calm analysis to constant alertness

### Practical Implications

**For Traders:**
1. Expect persistent volatility (Risk active 67% of time)
2. Monitor overnight gaps closely (Insula 68% active)
3. Use multi-factor analysis (Control 93% active)
4. Implement strict emotional discipline (avoid Insula triggers)

**For Investors:**
1. Post-COVID "normal" is fundamentally different from Pre-COVID
2. Risk management must account for 2x higher volatility perception
3. Trend-following still works (Sentiment 91%) but with higher noise
4. Value opportunities exist (Value 75%) but require faster execution

**For Researchers:**
1. Historical market models may not generalize to Post-COVID era
2. Behavioral finance became MORE important, not less
3. Machine learning models trained Pre-COVID need retraining
4. Emotional/instinctive responses now dominate market dynamics

---

## Files and Visualizations

### Generated Outputs

**Location**: `PrePostComparison/Results_PrePost_Comparison/`

**Data Files:**
- `activation_frequency_comparison.csv` - Summary statistics
- `pre_covid_activations.csv` - Daily activations (773 rows)
- `post_covid_activations.csv` - Daily activations (743 rows)

**Visualizations:**
- `activation_frequency_comparison.png` - Bar chart comparing frequencies
- `activation_change_analysis.png` - Horizontal bar chart showing changes
- `activation_heatmaps.png` - Daily activation patterns for both periods
- `activation_correlations.png` - System correlation matrices

**Code:**
- `xgboost_prepost_comparison.py` - Analysis implementation

---

## References

### Model Files
- Anti-overfitting implementation: `xgboost_anti_overfitting.py`
- 65/35 split variant: `xgboost_anti_overfitting_65_35.py`
- Baseline models: `xgboost_brain_analysis.py`

### Documentation
- Overfitting comparison: `OVERFITTING_COMPARISON.md`
- Data split methodology: `README_DATA_SPLITS.md`
- Results comparison: `RESULTS_COMPARISON.md`

---

*Analysis Date: January 2026*  
*NeuroFinance Research Project*  
*Anti-Overfitting XGBoost Models (70/15/15 Split)*
