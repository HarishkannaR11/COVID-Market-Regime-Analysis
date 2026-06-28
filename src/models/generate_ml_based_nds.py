"""
Generate ML-Based NDS for Statistical Testing
==============================================

Purpose: Create NDS based on actual XGBoost predictions (not rule-based labels)
This ensures statistical tests validate the ML approach, not just the rules.

Key difference:
- Rule-based: Uses threshold logic directly
- ML-based: Uses trained XGBoost models to predict activation

Author: NeuroFinance Research
Date: February 2026
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("GENERATING ML-BASED NDS FROM XGBOOST PREDICTIONS")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================
print("\nStep 1: Loading data...")
df_pre = pd.read_csv('nifty_bank_pre_covid.csv')
df_post = pd.read_csv('nifty_bank_post_covid.csv')

df_pre['date'] = pd.to_datetime(df_pre['date'])
df_post['date'] = pd.to_datetime(df_post['date'])

print(f"✓ Pre-COVID:  {len(df_pre)} days")
print(f"✓ Post-COVID: {len(df_post)} days")

# ============================================================================
# ADD INSULA FEATURES
# ============================================================================
print("\nStep 2: Adding Insula features...")

def add_insula_features(df):
    """Add Insula brain system features"""
    df = df.copy()
    
    df['prev_close'] = df['close'].shift(1)
    df['gap_open'] = (df['open'] - df['prev_close']) / df['prev_close']
    df['intraday_range'] = (df['high'] - df['low']) / df['open']
    
    df['volume_ma_20'] = df['volume'].rolling(window=20).mean()
    df['volume_spike'] = df['volume'] / df['volume_ma_20']
    
    df['gap_open'] = df['gap_open'].fillna(0)
    df['volume_spike'] = df['volume_spike'].fillna(1.0)
    
    df = df.drop(['prev_close', 'volume_ma_20'], axis=1, errors='ignore')
    
    return df

df_pre = add_insula_features(df_pre)
df_post = add_insula_features(df_post)

print("✓ Features added")

# ============================================================================
# CREATE RULE-BASED LABELS FOR TRAINING
# ============================================================================
print("\nStep 3: Creating rule-based labels for training...")

def create_activation_labels(df, thresholds_dict=None):
    """Create activation labels using rule-based thresholds"""
    df = df.copy()
    
    # Calculate thresholds on this data if not provided
    if thresholds_dict is None:
        thresholds_dict = {}
        
        # Value system
        thresholds_dict['value'] = {
            'rsi_q75': df['rsi'].quantile(0.75),
            'momentum_std': df['momentum_30d'].std(),
            'return_std': df['daily_return'].std()
        }
        
        # Risk system
        thresholds_dict['risk'] = {
            'vol_median': df['volatility_20d'].median(),
            'vol_std': df['volatility_20d'].std(),
            'return_std': df['daily_return'].std()
        }
        
        # Sentiment system
        thresholds_dict['sentiment'] = {
            'ma50_threshold': 0.02,
            'ma200_threshold': 0.03
        }
        
        # Insula system
        thresholds_dict['insula'] = {
            'gap_std': df['gap_open'].std(),
            'range_median': df['intraday_range'].median(),
            'range_std': df['intraday_range'].std()
        }
    
    # Apply thresholds
    df['value_active'] = (
        (df['rsi'] > thresholds_dict['value']['rsi_q75']) |
        (abs(df['momentum_30d']) > thresholds_dict['value']['momentum_std'] * 0.8) |
        (abs(df['daily_return']) > thresholds_dict['value']['return_std'])
    ).astype(int)
    
    df['risk_active'] = (
        (df['volatility_20d'] > thresholds_dict['risk']['vol_median'] + 
         thresholds_dict['risk']['vol_std'] * 0.5) |
        (df['daily_return'] < -thresholds_dict['risk']['return_std'])
    ).astype(int)
    
    df['sentiment_active'] = (
        (abs(df['price_to_ma50']) > thresholds_dict['sentiment']['ma50_threshold']) |
        (abs(df['price_to_ma200']) > thresholds_dict['sentiment']['ma200_threshold'])
    ).astype(int)
    
    df['insula_active'] = (
        (abs(df['gap_open']) > thresholds_dict['insula']['gap_std']) |
        (df['intraday_range'] > thresholds_dict['insula']['range_median'] + 
         thresholds_dict['insula']['range_std'] * 0.5) |
        (df['volume_spike'] > 1.5)
    ).astype(int)
    
    df['control_active'] = (
        (df['value_active'] + df['risk_active'] + 
         df['sentiment_active'] + df['insula_active']) >= 2
    ).astype(int)
    
    return df, thresholds_dict

# Split pre-COVID for training (70% train, 30% will be used for ML prediction)
split_idx = int(len(df_pre) * 0.7)
df_pre_train = df_pre.iloc[:split_idx].copy()
df_pre_test = df_pre.iloc[split_idx:].copy()

# Create labels on training data to get thresholds
df_pre_train, thresholds = create_activation_labels(df_pre_train, thresholds_dict=None)

# Apply same thresholds to all data (for training purposes)
df_pre_test, _ = create_activation_labels(df_pre_test, thresholds_dict=thresholds)
df_post, _ = create_activation_labels(df_post, thresholds_dict=thresholds)

print("✓ Activation labels created")

# ============================================================================
# TRAIN XGBOOST MODELS
# ============================================================================
print("\nStep 4: Training XGBoost models...")

# Feature columns
exclude_cols = ['date', 'dividends', 'stock_splits', 'value_active', 'risk_active', 
                'sentiment_active', 'insula_active', 'control_active']
feature_cols = [col for col in df_pre_train.columns if col not in exclude_cols]

X_train = df_pre_train[feature_cols]
models = {}

for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
    print(f"  Training {system}...", end=" ")
    
    y_train = df_pre_train[f'{system}_active']
    
    # Check if we have both classes
    if len(y_train.unique()) < 2:
        print(f"⚠ Only one class present, skipping ML training")
        models[system] = None
        continue
    
    model = xgb.XGBClassifier(
        max_depth=3,
        learning_rate=0.05,
        n_estimators=200,
        reg_alpha=1.0,
        reg_lambda=2.0,
        subsample=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    
    # Replace inf values
    X_train_clean = X_train.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    model.fit(X_train_clean, y_train, verbose=False)
    models[system] = model
    
    # Check training accuracy
    y_pred = model.predict(X_train_clean)
    acc = accuracy_score(y_train, y_pred)
    print(f"✓ Train Acc: {acc:.1%}")

# ============================================================================
# GENERATE ML-BASED PREDICTIONS FOR ENTIRE DATASET
# ============================================================================
print("\nStep 5: Generating ML-based predictions...")

def predict_ml_activations(df, models, feature_cols):
    """Use trained ML models to predict activations"""
    df = df.copy()
    
    X = df[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0)
    
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        if models[system] is not None:
            # Use ML predictions
            df[f'{system}_active_ml'] = models[system].predict(X)
        else:
            # Fallback to rule-based if ML not available
            df[f'{system}_active_ml'] = df[f'{system}_active']
    
    # Recompute control based on ML predictions
    df['control_active_ml'] = (
        (df['value_active_ml'] + df['risk_active_ml'] + 
         df['sentiment_active_ml'] + df['insula_active_ml']) >= 2
    ).astype(int)
    
    return df

# Predict for all data
df_pre_full = pd.concat([df_pre_train, df_pre_test], ignore_index=True).sort_values('date').reset_index(drop=True)
df_pre_ml = predict_ml_activations(df_pre_full, models, feature_cols)
df_post_ml = predict_ml_activations(df_post, models, feature_cols)

print("✓ ML predictions generated")

# ============================================================================
# COMPUTE ML-BASED NDS
# ============================================================================
print("\nStep 6: Computing ML-based NDS...")

def compute_nds_ml(df):
    """Compute NDS based on ML predictions"""
    nds = (
        df['value_active_ml'] * 1 +
        df['risk_active_ml'] * (-1) +
        df['sentiment_active_ml'] * 1 +
        df['insula_active_ml'] * (-1) +
        df['control_active_ml'] * 1
    )
    return nds

df_pre_ml['NDS_ML'] = compute_nds_ml(df_pre_ml)
df_post_ml['NDS_ML'] = compute_nds_ml(df_post_ml)

# Also compute rule-based NDS for comparison
df_pre_ml['NDS_Rule'] = (
    df_pre_ml['value_active'] * 1 +
    df_pre_ml['risk_active'] * (-1) +
    df_pre_ml['sentiment_active'] * 1 +
    df_pre_ml['insula_active'] * (-1) +
    df_pre_ml['control_active'] * 1
)

df_post_ml['NDS_Rule'] = (
    df_post_ml['value_active'] * 1 +
    df_post_ml['risk_active'] * (-1) +
    df_post_ml['sentiment_active'] * 1 +
    df_post_ml['insula_active'] * (-1) +
    df_post_ml['control_active'] * 1
)

print(f"✓ Pre-COVID ML-NDS:   Mean={df_pre_ml['NDS_ML'].mean():.3f}, Std={df_pre_ml['NDS_ML'].std():.3f}")
print(f"✓ Post-COVID ML-NDS:  Mean={df_post_ml['NDS_ML'].mean():.3f}, Std={df_post_ml['NDS_ML'].std():.3f}")
print(f"  Pre-COVID Rule-NDS:  Mean={df_pre_ml['NDS_Rule'].mean():.3f}, Std={df_pre_ml['NDS_Rule'].std():.3f}")
print(f"  Post-COVID Rule-NDS: Mean={df_post_ml['NDS_Rule'].mean():.3f}, Std={df_post_ml['NDS_Rule'].std():.3f}")

# ============================================================================
# SAVE COMBINED DATA
# ============================================================================
print("\nStep 7: Saving ML-based data...")

# Combine periods
df_combined_ml = pd.concat([df_pre_ml, df_post_ml], ignore_index=True)

# Save
df_combined_ml.to_csv('brain_activation_combined_xgboost_ML.csv', index=False)
print("✓ Saved: brain_activation_combined_xgboost_ML.csv")

# Also save separate periods
df_pre_ml.to_csv('brain_activation_pre_covid_ML.csv', index=False)
df_post_ml.to_csv('brain_activation_post_covid_ML.csv', index=False)
print("✓ Saved: brain_activation_pre_covid_ML.csv")
print("✓ Saved: brain_activation_post_covid_ML.csv")

# ============================================================================
# COMPARISON SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ML vs RULE-BASED NDS COMPARISON")
print("="*80)

# Agreement between ML and Rule-based
for period, df in [("Pre-COVID", df_pre_ml), ("Post-COVID", df_post_ml)]:
    print(f"\n{period}:")
    print("-" * 40)
    
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        agreement = (df[f'{system}_active'] == df[f'{system}_active_ml']).mean() * 100
        print(f"  {system.capitalize():<12} Agreement: {agreement:>5.1f}%")
    
    nds_agreement = (df['NDS_ML'] == df['NDS_Rule']).mean() * 100
    nds_corr = df['NDS_ML'].corr(df['NDS_Rule'])
    print(f"  {'NDS':<12} Agreement: {nds_agreement:>5.1f}%  Correlation: {nds_corr:.3f}")

print("\n" + "="*80)
print("READY FOR ML-BASED STATISTICAL TESTING")
print("="*80)
print("\nNext steps:")
print("  1. Run: python comprehensive_statistical_validation_ML.py")
print("  2. Run: python create_comprehensive_statistical_figure_ML.py")
print("="*80 + "\n")
