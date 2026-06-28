# NDS Distribution Analysis: Mentor Review Document

**Analysis Period:** 2017-2023 (1,516 trading days)  
**Pre-COVID:** 773 days | **Post-COVID:** 743 days  
**Date Prepared:** January 7, 2026

---

## Results Overview

This document presents the Neuro-Decision Score (NDS) distribution analysis comparing Pre-COVID and Post-COVID market periods. NDS is computed as a composite signal from three continuous market indicators:

**NDS Formula:**  
NDS(t) = Value_norm(t) - Risk_norm(t) + Sentiment_norm(t)

Where:
- **Value signal** = daily_return (market momentum)
- **Risk signal** = volatility_20d (market uncertainty)  
- **Sentiment signal** = (price - MA200) / MA200 (trend deviation)

All signals are z-score normalized using Pre-COVID statistics only.

---

## Statistical Summary

| Metric | Pre-COVID | Post-COVID | Change |
|--------|-----------|------------|--------|
| Mean | 0.000 | -2.010 | -2.010 |
| Median | 0.184 | -0.898 | -1.082 |
| Std Dev | 2.014 | 4.853 | +2.839 |
| Skewness | -0.855 | -2.009 | -1.154 |

**Statistical Tests:**
- Kolmogorov-Smirnov: D=0.246, p=1.08×10⁻²⁰ ✓ Significant
- Mann-Whitney U: p=1.97×10⁻¹⁸ ✓ Significant  
- Independent t-test: t=10.60, p=2.30×10⁻²⁵ ✓ Significant

---

## Graph 1: Kernel Density Estimate (KDE) - Distribution Shift

![NDS KDE Distribution](nds_distribution_kde.png)

### What this graph represents
Smoothed probability density functions showing the distribution shape of NDS values for Pre-COVID (blue) and Post-COVID (red) periods. Vertical dashed lines mark the mean values.

### What the graph shows
- Pre-COVID distribution centers near zero (μ=0.000, σ=1.979)
- Post-COVID distribution shifts leftward (μ=-0.885, σ=2.743)
- Mean shift: -0.885 (Cohen's d = -0.370, small-to-medium effect)
- Post-COVID shows wider spread (increased standard deviation)
- Post-COVID has extended left tail (more extreme negative values)

### What this graph does NOT claim
- Does not attribute causality to specific events
- Does not predict future distribution patterns
- Does not recommend trading strategies
- Does not claim one distribution is "better" or "worse"

---

## Graph 2: Q-Q Plot - Quantile Comparison

![NDS Q-Q Plot](nds_distribution_qqplot.png)

### What this graph represents
Quantile-Quantile plot comparing Pre-COVID NDS quantiles (x-axis) against Post-COVID NDS quantiles (y-axis). Red dashed line represents the reference where both distributions would be identical.

### What the graph shows
- Most points fall **below** the reference line, indicating Post-COVID values are systematically lower than Pre-COVID at corresponding quantiles
- Lower tail shows larger deviations (extreme negative values more common post-COVID)
- Upper tail follows reference line more closely
- Deviation pattern confirms leftward distributional shift

### What this graph does NOT claim
- Does not explain why the shift occurred
- Does not predict duration of the shift
- Does not suggest distributional convergence or divergence in future
- Does not imply market inefficiency

---

## Graph 3: Histogram Comparison - Frequency Distribution

![NDS Histogram](nds_distribution_histogram.png)

### What this graph represents
Overlapping histograms showing frequency distribution of NDS values with 50 bins. Pre-COVID (blue, n=724) and Post-COVID (red, n=694). Vertical dashed lines mark mean values.

### What the graph shows
- Pre-COVID concentrates around zero (narrow peak)
- Post-COVID shows broader, flatter distribution centered around -0.885
- Post-COVID has higher frequency in negative NDS range (-5 to -2)
- Post-COVID extends to more extreme negative values (beyond -15)
- K-S Test: D=0.2110, p=2.66×10⁻¹⁴ (highly significant difference)

### What this graph does NOT claim
- Does not claim distributions are permanently changed
- Does not attribute frequency changes to specific market mechanisms
- Does not suggest optimal NDS thresholds
- Does not recommend portfolio adjustments

---

## Graph 4: Box Plot Comparison - Summary Statistics

![NDS Box Plot](nds_boxplot_comparison.png)

### What this graph represents
Box-and-whisker plots summarizing the distribution of NDS through quartiles, median, and outliers for both periods.

### What the graph shows
- Pre-COVID median: 0.184 (solid line in blue box)
- Post-COVID median: -0.898 (solid line in red box)  
- Median shift: -1.082
- Post-COVID shows larger interquartile range (IQR) - wider box
- Post-COVID has more extreme lower outliers (below whisker)
- Both periods show negative skew (longer lower whisker)

### What this graph does NOT claim
- Does not identify causes of median shift
- Does not predict median reversion
- Does not classify outliers as "anomalous" or "normal"
- Does not suggest outlier removal

---

## Graph 5: Time Series Evolution - NDS Over Time

![NDS Time Series](nds_time_series.png)

### What this graph represents
Daily NDS values plotted chronologically from 2017 to 2023, with COVID-19 onset marked by vertical red line (March 2020). Blue region = Pre-COVID, Red region = Post-COVID.

### What the graph shows
- Pre-COVID (2017-March 2020): Fluctuations around zero baseline
- Post-COVID (March 2020-2023): Increased volatility and sustained negative values
- March 2020: Sharp negative spike coinciding with COVID onset
- Post-March 2020: NDS remains predominantly below zero
- Extreme negative values (-30+) occur exclusively in Post-COVID period

### What this graph does NOT claim
- Does not establish COVID-19 as sole cause of NDS shift
- Does not predict when/if NDS will return to Pre-COVID levels
- Does not suggest regime change is permanent
- Does not recommend timing strategies based on NDS levels

---

## Expected Questions

### Q1: What does the negative NDS shift mean in practical terms?
**A:** Post-COVID period shows systematically lower composite signal combining reduced daily returns, increased volatility, and more frequent price deviations below long-term trend.

### Q2: Why use Pre-COVID statistics only for normalization?
**A:** Using Pre-COVID statistics avoids look-ahead bias and provides consistent baseline for comparing how Post-COVID signals deviate from the established pre-pandemic regime.

### Q3: Are the statistical tests robust to non-normal distributions?
**A:** Yes. Mann-Whitney U test is non-parametric (no normality assumption). Kolmogorov-Smirnov directly tests distribution differences. All three tests converge on p<0.001, providing robust evidence.

### Q4: What is the Cohen's d effect size of -0.370?
**A:** Small-to-medium standardized effect size indicating mean shifted by 0.37 standard deviations. While statistically significant (large sample), the practical magnitude is moderate.

---

## Methodological Notes

**Data Source:** XGBoost brain activation model (brain_activation_combined_xgboost.csv)  
**Normalization:** Z-score using Pre-COVID μ and σ only  
**Equal Weighting:** w₁=w₂=w₃=1.0 (simple, defensible baseline)  
**Missing Values:** None (0% missing in all three signals)  
**Sample Sizes:** Pre=773 days, Post=743 days (unequal, handled by tests)

**Analysis Limitations:**
- NDS is a constructed metric, not directly observable
- Equal weighting is simplifying assumption
- Distribution shift does not imply causality
- Results specific to Nifty Bank Index 2017-2023

---

**Document Purpose:** Results presentation only. No trading recommendations. No causal claims beyond observed statistical associations.
