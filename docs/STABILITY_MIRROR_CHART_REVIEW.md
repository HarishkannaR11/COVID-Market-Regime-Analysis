****# System Stability Analysis: Mentor Review

**Analysis Method:** XGBoost Brain Activation Model  
**Metric:** Run Length (consecutive days systems stay activated)  
**Data Period:** January 2017 – February 2023 (1,516 trading days)  
**Pre-COVID:** January 2017 – February 2020 (773 days)  
**Post-COVID:** March 2020 – February 2023 (743 days)  

---

## Graph: System Stability Mirror Chart

![System Stability Mirror Chart](stability_mirror_chart.png)

---

### What This Graph Represents

Butterfly/mirror chart comparing average run lengths between Pre-COVID (blue, left side) and Post-COVID (red, right side) periods. **Run length** measures state persistence: the average number of consecutive days each cognitive system remains in activated (ON) state before switching to inactive (OFF) state.

- **Left bars (blue):** Pre-COVID run lengths
- **Right bars (red):** Post-COVID run lengths  
- **Center labels (green):** Percentage change from Pre to Post
- **Bar length:** Indicates stability level (longer = more stable/persistent)

Each system's activation status determined by XGBoost binary classification (0 = inactive, 1 = active). Run lengths computed by counting consecutive sequences of 1s in the activation data.

---

### What The Graph Shows

**State Persistence Metrics:**

| System | Pre-COVID Run Length | Post-COVID Run Length | Change | Interpretation |
|--------|---------------------|----------------------|--------|----------------|
| **Sentiment** | 20.1 days | 30.6 days | **+52.7%** | Most stable; stays activated ~1 month on average |
| **Control** | 7.3 days | 9.4 days | +28.3% | Second-most stable; ~9-10 day activation periods |
| **Insula** | 2.4 days | 2.9 days | +18.8% | Least stable; frequent switching (~3 days) |
| **Value** | 4.8 days | 5.6 days | +15.6% | Moderate stability; ~5-6 day periods |
| **Risk** | 4.3 days | 4.5 days | +5.0% | Smallest increase; minimal stability change |

**Key Observations:**

1. **Universal Increase:** All five systems show increased persistence post-COVID (all positive changes)

2. **Sentiment Dominance:** Sentiment system exhibits dramatically longer activation runs post-COVID, increasing from approximately 3 weeks to 1 month average duration

3. **Stability Hierarchy:** Systems rank consistently by stability level:
   - **High:** Sentiment (30.6d) >> Control (9.4d)
   - **Moderate:** Value (5.6d), Risk (4.5d)
   - **Low:** Insula (2.9d)

4. **Visual Impact:** Bar length differences clearly demonstrate Sentiment's exceptional stability compared to other systems, with its Post-COVID bar extending significantly beyond all others

5. **Magnitude Variation:** Percentage changes range from +5.0% (Risk) to +52.7% (Sentiment), indicating heterogeneous stability responses across cognitive systems

---

### What This Graph Does NOT Claim

**Causality:**  
- Does not establish that COVID-19 **caused** increased run lengths
- Other concurrent factors (monetary policy, market structure changes, volatility regimes) not examined
- Correlation observed between time periods, not causation proven

**Mechanism:**  
- Does not explain **why** systems became more stable
- Does not identify specific features or market conditions driving persistence changes
- No attribution to investor psychology, sentiment dynamics, or behavioral factors

**Prediction:**  
- Does not forecast future run lengths or stability patterns
- Historical increases do not guarantee continued stability
- No forward-looking projections made

**Optimality:**  
- Does not claim longer run lengths indicate better system performance
- Does not suggest high stability is superior to low stability
- No normative judgment about optimal persistence levels

**Trading Signal:**  
- Stability metrics are descriptive observations, not actionable recommendations
- No investment strategy implied or suggested
- Academic research purpose only; not trading advice

**Generalization:**  
- Findings specific to Nifty Bank Index (2017-2023)
- Generalizability to other markets, assets, or time periods unknown
- Single-dataset analysis without cross-market validation

---

## Expected Questions

**Q1: Why did Sentiment show the largest stability increase (+52.7%)?**  
**A:** Sentiment system may respond to persistent narratives or information regimes that became more stable post-COVID. Specific mechanism unclear; could reflect sustained market trends, changes in news flow persistence, or altered feature correlations. Causal explanation requires additional analysis.

**Q2: Is the +52.7% increase statistically significant?**  
**A:** Formal significance testing not performed. Value represents observed average across 773 Pre-COVID and 743 Post-COVID days. Hypothesis testing with appropriate null model would be required for statistical inference.

**Q3: Are these findings robust to methodological choices?**  
**A:** Yes. Window size sensitivity analysis shows consistent positive changes across six different smoothing windows (Raw, 15d, 30d, 45d, 60d, 90d). System rankings remain stable across all specifications.

**Q4: What does "run length" measure exactly?**  
**A:** Run length counts consecutive days a system stays activated (value=1) before switching to inactive (value=0). For example, sequence [1,1,1,0,1,1] contains two runs: length 3 and length 2. Average run length is mean of all such sequences in the period.

---

## Technical Notes

**Computation Method:**  
- Raw binary activation data (0/1) from XGBoost model
- Consecutive 1s grouped using itertools.groupby algorithm
- Run lengths calculated as length of each activation sequence
- Averages computed separately for Pre-COVID and Post-COVID periods

**No Smoothing Applied:**  
- Run lengths computed on raw binary data without rolling window smoothing
- Represents actual consecutive activation days, not smoothed regime scores

**Data Characteristics:**  
- Pre-COVID: 773 observations (2017-01-03 to 2020-02-28)
- Post-COVID: 743 observations (2020-03-02 to 2023-02-28)
- Binary activations: 0=inactive, 1=active (XGBoost threshold-based classification)

**Limitations:**  
- Descriptive statistics only; no inferential testing
- Single dataset; external validity unknown
- Temporal autocorrelation not explicitly modeled
- No adjustment for multiple comparisons across 5 systems

---

## Summary

**Main Finding:** All cognitive systems exhibited increased state persistence (longer average activation runs) in the Post-COVID period compared to Pre-COVID, with Sentiment system showing the most dramatic stability increase (+52.7%).

**Interpretation:** The observed pattern suggests structural changes in cognitive system activation dynamics following March 2020, characterized by less frequent switching and more sustained activation states.

**Limitation:** Analysis is descriptive and observational. Causality, mechanism, and predictive value not established.

---

**Document prepared for:** Mentor Review  
**Date:** January 2026  
**Analysis type:** Descriptive Statistics  
**Data source:** Nifty Bank Index, XGBoost Brain Activation Model (5 systems)
