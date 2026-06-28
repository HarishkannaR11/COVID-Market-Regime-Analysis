3# NEUROFINANCE XGBOOST BRAIN SYSTEM ANALYSIS - DOCUMENTATION

## 📋 Overview

**Purpose:** Identify which brain systems (Value/Risk/Sentiment/Insula/Control) are ACTIVE during different market conditions using XGBoost machine learning.

**Research Question:** How do brain activation patterns differ between Pre-COVID (2017-2020) and Post-COVID (2020-2023) market regimes?

---

## 🧠 Brain System Architecture

### **1. VALUE SYSTEM (vmPFC - Ventromedial Prefrontal Cortex)**
**Function:** Reward processing, value assessment, opportunity detection

**Features:**
- `rsi` - Relative Strength Index (overbought/oversold)
- `momentum_30d` - 30-day price momentum
- `daily_return` - Daily price change
- `weekly_return` - Weekly price change  
- `monthly_return` - Monthly price change

**Activation Triggers:**
- RSI > 70 (overbought) OR RSI < 30 (oversold)
- Strong momentum (> 1 standard deviation)
- Significant returns (> 1.5 standard deviations)

---

### **2. RISK SYSTEM (Amygdala)**
**Function:** Threat detection, fear response, uncertainty processing

**Features:**
- `volatility_20d` - 20-day rolling volatility
- `daily_return` - For extreme loss detection

**Activation Triggers:**
- High volatility (> median + 1 SD)
- Extreme losses (< -2 standard deviations)

---

### **3. SENTIMENT SYSTEM (dmPFC - Dorsomedial Prefrontal Cortex)**
**Function:** Trend perception, social consensus, market sentiment

**Features:**
- `price_to_ma50` - Price deviation from 50-day moving average
- `price_to_ma200` - Price deviation from 200-day moving average
- `above_ma_50` - Binary trend indicator
- `above_ma_200` - Binary long-term trend indicator

**Activation Triggers:**
- Strong deviation from moving averages (> 5%)
- Trend shifts (crossing MA levels)

---

### **4. INSULA SYSTEM (Interoception)**
**Function:** Gut feelings, bodily states, intuitive signals, loss aversion

**Features:**
- `gap_open` - Opening gap from previous close (overnight shock)
- `intraday_range` - (High - Low) / Open (intraday chaos)
- `volume_spike` - Volume / 20-day average volume (panic/euphoria)

**Activation Triggers:**
- Significant overnight gaps (> 1.5 SD)
- High intraday range (> median + 1 SD)
- Volume surge (> 2x average)

---

### **5. CONTROL SYSTEM (dlPFC - Dorsolateral Prefrontal Cortex)**
**Function:** Executive coordination, decision making under conflict

**Activation Trigger:**
- Activated when 2+ other brain systems are simultaneously active
- Indicates complex decision-making situation

---

## 📊 Dataset Specifications

### **Pre-COVID Period**
- **Date Range:** January 3, 2017 → February 28, 2020
- **Duration:** 37 months (3 years, 1 month)
- **Rows:** 773 trading days
- **Features:** 25 (22 original + 3 Insula features)
- **Missing Values:** 0

### **Post-COVID Period**
- **Date Range:** March 2, 2020 → February 28, 2023
- **Duration:** 37 months (3 years, 1 month)
- **Rows:** 743 trading days
- **Features:** 25 (22 original + 3 Insula features)
- **Missing Values:** 0

### **Balance:** 96.1% (Excellent)

---

## 🔬 Methodology

### **Step 1: Feature Engineering**
Add 3 Insula features to existing 22 features:
```python
gap_open = (open - previous_close) / previous_close
intraday_range = (high - low) / open
volume_spike = volume / rolling_avg_volume_20d
```

### **Step 2: Brain Activation Detection**
For each day, determine if each brain system is ACTIVE (binary: 1 or 0)
- Apply threshold rules to each feature
- System is active if ANY feature exceeds threshold

### **Step 3: XGBoost Training**
Train 5 separate XGBoost binary classifiers:
1. Value System classifier
2. Risk System classifier
3. Sentiment System classifier
4. Insula System classifier
5. Control System classifier

**XGBoost Parameters:**
- `max_depth`: 5 (tree depth)
- `learning_rate`: 0.1
- `n_estimators`: 100 (number of trees)
- `tree_method`: 'hist' (CPU-optimized)

### **Step 4: Feature Importance Analysis**
Extract which features drive each brain system activation

### **Step 5: Regime Comparison**
Compare activation frequencies Pre-COVID vs Post-COVID

---

## 🚀 How to Run

### **Prerequisites**
```bash
pip install xgboost pandas numpy matplotlib seaborn scikit-learn
```

### **Execution**
```bash
cd "c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels"
python xgboost_brain_analysis.py
```

### **Expected Runtime**
- **i5 CPU:** 5-10 seconds total
- **Memory:** <200 MB
- **Output:** 4 CSV files + 6 PNG visualizations

---

## 📁 Output Files

### **CSV Files:**

1. **brain_activation_pre_covid.csv**
   - Pre-COVID data with activation labels
   - Columns: 25 features + 5 activation labels (value_active, risk_active, etc.)

2. **brain_activation_post_covid.csv**
   - Post-COVID data with activation labels
   - Same structure as Pre-COVID

3. **brain_activation_summary.csv**
   - Summary statistics for all brain systems
   - Columns: Regime, Brain_System, Activation_Frequency_%, Total_Active_Days, Total_Days

### **Visualization Files (Plots-XGBoost/):**

1. **feature_importance_all_systems.png**
   - Bar charts showing top 10 features for each brain system
   - 6 subplots (5 brain systems + control)

2. **activation_frequency_comparison.png**
   - Bar chart comparing activation frequencies Pre vs Post COVID
   - Shows % of days each system was active

3. **activation_timeline_pre-covid.png**
   - Timeline showing when each brain system activated (Pre-COVID)
   - 5 stacked time series plots

4. **activation_timeline_post-covid.png**
   - Timeline showing when each brain system activated (Post-COVID)
   - 5 stacked time series plots

---

## 📈 Interpreting Results

### **Activation Frequency**
- **High frequency (>50%):** System frequently engaged
- **Medium frequency (25-50%):** System moderately active
- **Low frequency (<25%):** System rarely triggered

### **Pre vs Post Comparison**

**Expected Patterns:**
- **Risk System:** Higher activation Post-COVID (more volatility)
- **Insula System:** Higher activation Post-COVID (more gut-feeling moments)
- **Value System:** May decrease Post-COVID (less clear opportunities)
- **Sentiment System:** May shift (different trend patterns)

### **Feature Importance**

**High importance (>0.15):** Critical driver of brain activation
**Medium importance (0.05-0.15):** Moderate influence
**Low importance (<0.05):** Minor influence

---

## 🎯 Research Applications

### **1. Market Psychology**
- Understand which mental processes dominate different market regimes
- Identify stress periods (high Risk + Insula activation)

### **2. Decision Making**
- Detect when traders need executive control (Control system active)
- Identify automatic vs deliberate decision periods

### **3. Regime Characterization**
- Pre-COVID: Value-driven markets?
- Post-COVID: Fear-driven markets?

### **4. Trading Strategy**
- High Risk activation → Reduce position sizes
- High Value activation → Look for opportunities
- High Insula activation → Trust intuition cautiously

---

## 🔧 Technical Specifications

### **Why XGBoost?**
✅ Handles non-normal distributions (your data has skewness)  
✅ Handles outliers (12.9% in price_to_ma200)  
✅ No normalization needed (scale-invariant)  
✅ Fast CPU training (1-2 seconds on i5)  
✅ Feature importance (interpretable)  
✅ High accuracy (75-85% expected)

### **Algorithm Advantages Over Logistic Regression:**
| Metric | Logistic Regression | XGBoost |
|--------|---------------------|---------|
| Accuracy | 64-82% | 75-85% |
| Handles non-normal data | ❌ Poor | ✅ Excellent |
| Handles outliers | ❌ Sensitive | ✅ Robust |
| Interpretability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Training speed | <1 sec | 1-2 sec |

---

## 📊 Sample Results Structure

### **brain_activation_summary.csv:**
```
Regime      | Brain_System | Activation_Frequency_% | Total_Active_Days | Total_Days
------------|--------------|------------------------|-------------------|------------
Pre-COVID   | Value        | 45.2                   | 349              | 773
Pre-COVID   | Risk         | 23.1                   | 178              | 773
Pre-COVID   | Sentiment    | 62.8                   | 485              | 773
Pre-COVID   | Insula       | 18.5                   | 143              | 773
Pre-COVID   | Control      | 35.6                   | 275              | 773
Post-COVID  | Value        | 41.7                   | 310              | 743
Post-COVID  | Risk         | 38.5                   | 286              | 743  ← INCREASED
Post-COVID  | Sentiment    | 58.3                   | 433              | 743
Post-COVID  | Insula       | 29.2                   | 217              | 743  ← INCREASED
Post-COVID  | Control      | 42.1                   | 313              | 743  ← INCREASED
```

---

## 🐛 Troubleshooting

### **Error: "No module named 'xgboost'"**
```bash
pip install xgboost
```

### **Error: "File not found"**
Ensure you're in the correct directory:
```bash
cd "c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels"
```

### **Low Accuracy (<60%)**
- Check class imbalance (some systems may activate <10% of time)
- Try adjusting threshold rules in BRAIN_SYSTEMS config
- Increase n_estimators to 200

### **Memory Issues**
- Reduce max_depth to 4
- Reduce n_estimators to 50
- Process one regime at a time

---

## 📚 References

### **Neuroeconomics Foundations:**
- **vmPFC (Value):** Rangel & Hare (2010) - Simple computations in choice
- **Amygdala (Risk):** De Martino et al. (2010) - Frames and emotional arousal
- **dmPFC (Sentiment):** Hampton et al. (2008) - Social information in decision-making
- **Insula (Gut Feeling):** Kuhnen & Knutson (2005) - Anticipatory affect in risk-taking
- **dlPFC (Control):** Hare et al. (2009) - Self-control in decision-making

### **XGBoost:**
- Chen & Guestrin (2016) - XGBoost: A Scalable Tree Boosting System

---

## 📧 Support

For questions or issues:
- Check console output for detailed error messages
- Verify CSV files are in correct directory
- Ensure Python 3.8+ is installed

---

## 📄 License

Research use only. NeuroFinance Brain System Analysis © 2026

---

**Created:** January 2026  
**Version:** 1.0  
**Platform:** Windows i5 CPU-optimized
