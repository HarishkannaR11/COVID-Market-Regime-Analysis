
This folder contains experiments with different train/validation/test split ratios to evaluate model performance and generalization.

## Overview

All experiments use **XGBoost classifiers** to detect brain system activation (Value, Risk, Sentiment, Insula, Control) with **NO DATA LEAKAGE**:
- Activation thresholds calculated **only** from training data
- Same thresholds applied to validation and test sets
- Truly independent evaluation

---

## Experiment 1: 70/15/15 Split (Baseline)

**File**: `../xgboost_brain_analysis.py` (main implementation)

### Data Split
- **Training**: 70% (1,061 samples)
- **Validation**: 15% (227 samples)
- **Test**: 15% (228 samples)

### Results Summary

| System | Validation Accuracy | Test Accuracy | Val ROC AUC | Test ROC AUC |
|--------|-------------------|---------------|-------------|--------------|
| Value | 97.4% | 95.6% | 0.9919 | 0.9906 |
| Risk | 90.7% | 96.1% | 0.9858 | 0.9625 |
| Sentiment | 100.0% | 97.8% | 1.0000 | 0.9930 |
| Insula | 92.1% | 96.1% | 0.9767 | 0.9802 |
| Control | 95.2% | 97.8% | 0.9868 | 0.9973 |

### Key Insights
- **Best balance** between training data (70%) and evaluation sets (30% total)
- **Consistent performance** across validation and test (90-100%)
- **Sentiment System** achieves perfect validation accuracy (100%)
- **Control System** shows highest test ROC AUC (0.9973)

### Pros
✓ More training data = better pattern learning  
✓ Sufficient validation/test data for reliable evaluation  
✓ Industry standard split ratio

### Cons
✗ Smaller test set may have higher variance

---

## Experiment 2: 65/35 Split

**File**: `xgboost_split_65_35.py`

### Data Split
- **Training**: 65% (~985 samples)
- **Validation**: 17.5% (~265 samples)
- **Test**: 17.5% (~265 samples)

### Purpose
- **More conservative** split with larger evaluation sets
- Test if models maintain performance with **5% less training data**
- Larger test set for **more stable** performance estimates

### How to Run
```bash
cd DataSplitExperiments
python xgboost_split_65_35.py
```

### Output Files
- `Results_65_35/model_performance_65_35.csv` - Accuracy and ROC AUC metrics
- `Results_65_35/split_information_65_35.csv` - Data split details

### Expected Trade-offs
- **Slightly lower training accuracy** (less data to learn from)
- **More stable test metrics** (larger test set)
- **Better validation of generalization** (more unseen data)

---

## Experiment 3: 60/40 Split

**File**: `xgboost_split_60_40.py`

### Data Split
- **Training**: 60% (~910 samples)
- **Validation**: 20% (~303 samples)
- **Test**: 20% (~303 samples)

### Purpose
- **Maximum evaluation data** (40% total)
- Test model robustness with **10% less training data** than baseline
- Verify if patterns are learnable with **smaller training set**

### How to Run
```bash
cd DataSplitExperiments
python xgboost_split_60_40.py
```

### Output Files
- `Results_60_40/model_performance_60_40.csv` - Accuracy and ROC AUC metrics
- `Results_60_40/split_information_60_40.csv` - Data split details

### Expected Trade-offs
- **Lower training accuracy** (least training data)
- **Most stable test metrics** (largest test set - 303 samples)
- **Stronger generalization test** (models must learn efficiently)

---

## Comparison Framework

### When to Use Each Split

**70/15/15 (Baseline)** - Recommended for:
- Standard model development
- Maximum training performance
- Balanced approach

**65/35 Split** - Recommended for:
- Conservative validation
- Larger test sets for stability
- Research publications requiring robust evaluation

**60/40 Split** - Recommended for:
- Small datasets where every test sample matters
- Maximum confidence in generalization
- Testing learning efficiency

### Evaluation Criteria

Compare all three experiments on:

1. **Training Accuracy** - How well does model fit training data?
2. **Validation Accuracy** - Does model generalize to validation?
3. **Test Accuracy** - Final performance on held-out test set
4. **ROC AUC Scores** - Discrimination ability (>0.95 excellent)
5. **Consistency** - Val vs Test difference (<5% is good)

---

## Data Leakage Prevention

All experiments implement **strict data leakage prevention**:

### Activation Threshold Calculation
```python
# Step 1: Calculate thresholds ONLY from training data
df_train, thresholds = create_activation_labels(df_train, thresholds_dict=None)

# Step 2: Apply SAME thresholds to validation (no leakage!)
df_val, _ = create_activation_labels(df_val, thresholds_dict=thresholds)

# Step 3: Apply SAME thresholds to test (no leakage!)
df_test, _ = create_activation_labels(df_test, thresholds_dict=thresholds)
```

### What This Prevents
✓ Test set statistics influencing activation labels  
✓ Models "seeing" future data during threshold calculation  
✓ Overly optimistic performance estimates

### Verification
- Check that activation frequencies differ between train/val/test
- Confirms thresholds are learned from training only
- Realistic performance on truly unseen data

---

## Running All Experiments

### Quick Start
```bash
# Navigate to DataSplitExperiments folder
cd "C:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels\DataSplitExperiments"

# Run 70/15/15 baseline (in parent directory)
cd ..
python xgboost_brain_analysis.py
cd DataSplitExperiments

# Run 65/35 split
python xgboost_split_65_35.py

# Run 60/40 split
python xgboost_split_60_40.py
```

### Results Comparison
After running all experiments, compare CSV files:
- `Results_65_35/model_performance_65_35.csv`
- `Results_60_40/model_performance_60_40.csv`
- `../brain_activation_summary.csv` (70/15/15 baseline)

---

## Key Findings (Expected)

Based on machine learning theory with ~1,500 total samples:

### Training Data Impact
- **70% (1,061 samples)**: Optimal learning, highest training accuracy
- **65% (985 samples)**: Minor decrease (<2%), still excellent
- **60% (910 samples)**: Noticeable decrease (~3-5%), but acceptable

### Test Set Stability
- **15% (228 samples)**: Moderate variance in metrics
- **17.5% (265 samples)**: Lower variance, more stable
- **20% (303 samples)**: Lowest variance, most reliable estimates

### Recommended Split
**70/15/15** for this dataset because:
- 1,061 training samples sufficient for XGBoost
- 228 test samples adequate for evaluation
- Best balance of learning vs evaluation
- Industry standard approach

---

## Technical Notes

### Random State
- All experiments use `random_state=42` for reproducibility
- Same random splits across all runs
- Fair comparison between split ratios

### Stratification
- Not currently implemented (can be added)
- Activation frequencies naturally balanced (48-85%)
- Stratification would ensure exact class proportions

### Brain Systems
All experiments evaluate 5 brain systems:
1. **Value System** (vmPFC) - Reward processing
2. **Risk System** (Amygdala) - Threat detection
3. **Sentiment System** (dmPFC) - Trend perception
4. **Insula System** - Gut feelings, interoception
5. **Control System** (dlPFC) - Executive coordination

---

## Citation

If using these experiments in research, document:
- Split ratio used (70/15/15, 65/35, or 60/40)
- Total samples: 1,516 (773 Pre-COVID + 743 Post-COVID)
- Random state: 42
- No data leakage: Thresholds from training only
- XGBoost version: 3.1.2

---

## Contact & Support

For questions about data split experiments:
1. Check output CSV files for detailed metrics
2. Compare validation vs test accuracy (should be within 5%)
3. Verify ROC AUC scores (>0.95 indicates excellent discrimination)
4. Review activation frequency distributions across splits

**Last Updated**: January 2026  
**Experiment Status**: Ready to run
