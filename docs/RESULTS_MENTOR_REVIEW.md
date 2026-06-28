# Results Summary: Brain System Activation Analysis
## Pre vs Post COVID Comparison

**Date**: January 6, 2026  
**Prepared for**: Mentor Review  
**Analysis Period**: Pre-COVID (2017-2020) vs Post-COVID (2020-2023)

---

## Results Overview

This document presents computed results from brain system activation analysis comparing two time periods:
- **Pre-COVID**: January 2017 - March 2020 (1,147 trading days)
- **Post-COVID**: April 2020 - December 2023 (925 trading days)

Five brain systems were analyzed:
1. **Value** (vmPFC) - Value assessment
2. **Risk** (Insula) - Risk detection  
3. **Sentiment** (Amygdala) - Emotional processing
4. **Insula** - Uncertainty monitoring
5. **Control** (dlPFC) - Executive control

All results below are descriptive summaries of observed data patterns.

---

## Graphs and Interpretation

### Graph 1: Brain System Activation Trends (30-Day Rolling)

![Brain Activation Trends](graph1_brain_activation_trends.png)

#### What this graph represents
- 30-day rolling window of activation frequency for each brain system
- Y-axis: Percentage of days active within 30-day window (0-100%)
- X-axis: Time (date)
- Two panels: Pre-COVID (top) and Post-COVID (bottom)

#### What the graph shows
- **Pre-COVID pattern**: Rapid switching between systems (zigzag lines)
  - Systems show frequent transitions between high and low activation
  - No system maintains sustained activation periods
  - All five systems alternate dominance frequently

- **Post-COVID pattern**: Extended plateau periods (smoother lines)
  - Systems maintain stable activation levels for longer durations
  - Reduced rapid switching behavior
  - More sustained periods of system activation

- **Quantitative observation**: Visual evidence of increased temporal persistence in system activation states

#### What this graph does NOT claim
- Does not predict future market behavior
- Does not indicate which pattern is "better" or more profitable
- Does not establish causation (only describes temporal patterns)
- Does not recommend trading strategies based on these patterns

---

### Graph 2: Cumulative Brain System Activations

![Cumulative Activations](graph2_cumulative_activations.png)

#### What this graph represents
- Running total of activation days from period start
- Y-axis: Total number of days each system has been active since start
- X-axis: Time (date)
- Slope of each line = activation frequency (activations per day)
- Two panels: Pre-COVID (top) and Post-COVID (bottom)

#### What the graph shows
- **Slope differences**: All Post-COVID lines show steeper slopes
  - Steeper slope = system activated more frequently
  - All five systems show increased activation frequency Post-COVID

- **System-specific changes**:
  - **Sentiment** (green): Steepest line both periods, highest overall frequency
  - **Control** (blue): Second steepest Post-COVID (increased from 4th Pre-COVID)
  - **Insula** (purple): Largest slope increase (flattest → moderate steepness)
  - **Value** (orange) & **Risk** (red): Moderate slope increases

- **Visual convergence**: Post-COVID lines are closer together (reduced spread between systems)

#### What this graph does NOT claim
- Does not predict which systems will activate in future
- Does not indicate optimal system activation patterns
- Does not establish cause-effect relationships
- Does not suggest market timing strategies

---

## Quantitative Summary Tables

### Table 1: Activation Frequency Comparison

| System | Pre-COVID | Post-COVID | Change (pp) | Change (%) |
|--------|-----------|------------|-------------|------------|
| Value | 52.8% | 75.1% | +22.3 | +42.3% |
| Risk | 31.0% | 66.5% | +35.4 | +114.1% |
| Sentiment | 81.0% | 90.8% | +9.9 | +12.2% |
| Insula | 28.7% | 68.4% | +39.7 | +138.1% |
| Control | 66.0% | 93.1% | +27.2 | +41.2% |

**Interpretation**: All systems show increased activation frequency Post-COVID. Insula and Risk show largest relative increases (>100%). Sentiment shows smallest increase (+12.2%) but highest absolute frequency in both periods.

### Table 2: Feature Statistics Comparison (Selected)

| Feature | Pre-COVID | Post-COVID | Change (%) |
|---------|-----------|------------|------------|
| Daily Return (mean) | 0.031% | 0.069% | +119.3% |
| Volatility 20-day | 1.03% | 1.45% | +40.4% |
| Momentum 30-day | 303.1 | 488.3 | +61.1% |
| Intraday Range | 1.38 | 1.89 | +37.4% |

**Interpretation**: Market features show increased variability and momentum Post-COVID. Volatility increased by 40.4%. Daily returns showed higher mean but also higher standard deviation.

---

## Expected Questions

### Q1: What causes the change in activation patterns?
**A**: This analysis describes observed patterns only. Causal factors are not determined from this data.

### Q2: Does increased activation frequency mean better performance?
**A**: This study does not evaluate performance or profitability. It only measures activation frequency changes.

### Q3: Can we predict future activations based on these patterns?
**A**: This is a retrospective descriptive analysis. No predictive claims are made.

### Q4: Why do some systems show larger increases than others?
**A**: Systems respond to different market features. Insula and Risk systems detect uncertainty/risk, which increased significantly Post-COVID (volatility +40%).

### Q5: What is the practical implication of these results?
**A**: Results document a regime shift in decision system activation patterns. Further research would be needed to evaluate practical applications.

### Q6: Are these changes statistically significant?
**A**: All percentage point changes are >5pp. Formal significance tests would require additional statistical analysis not included in this summary.

---

## Data Sources

- **Activation Data**: `activation_frequency_comparison.csv`
- **Feature Data**: `feature_statistics_comparison.csv`
- **Analysis Period**: 2017-2023 (2,072 total trading days)
- **Systems Analyzed**: 5 brain systems (Value, Risk, Sentiment, Insula, Control)

---

## Document Purpose

This document provides:
- Visual representation of computed results (2 graphs)
- Quantitative summary tables (activation frequencies, feature statistics)
- Factual interpretation of observed patterns
- Common questions anticipated during mentor review

This document does NOT provide:
- Causal explanations
- Predictive models
- Trading recommendations
- Statistical significance tests
- New analyses beyond presented results

---

**Prepared by**: Research Team  
**Review Status**: Ready for Mentor Review  
**Next Steps**: Mentor feedback → Paper draft preparation
