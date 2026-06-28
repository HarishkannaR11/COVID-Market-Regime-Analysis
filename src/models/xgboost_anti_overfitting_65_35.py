"""
ANTI-OVERFITTING XGBOOST IMPLEMENTATION - 65/35 SPLIT
======================================================

Enhancements to reduce overfitting:
1. Regularization parameters (L1/L2)
2. Early stopping
3. Reduced model complexity
4. Subsampling
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add parent directory to path
sys.path.append('..')
from xgboost_brain_analysis import (
    BRAIN_SYSTEMS, add_insula_features, detect_brain_activation, 
    create_activation_labels, plot_feature_importance
)

def train_brain_system_model_optimized(X_train, y_train, X_val, y_val, X_test, y_test, system_name):
    """
    Train XGBoost with anti-overfitting measures:
    - Reduced max_depth
    - L1/L2 regularization
    - Early stopping
    - Subsampling
    """
    
    print(f"\n{'='*60}")
    print(f"Training {system_name.upper()} System (Anti-Overfitting)")
    print(f"{'='*60}")
    
    # OPTIMIZED parameters to prevent overfitting
    params = {
        'max_depth': 3,                    # Reduced from 5 (shallower trees)
        'learning_rate': 0.05,             # Reduced from 0.1 (slower learning)
        'n_estimators': 200,               # Increased with early stopping
        'min_child_weight': 5,             # Increased from 1 (more conservative)
        'subsample': 0.8,                  # Random row sampling (NEW)
        'colsample_bytree': 0.8,          # Random feature sampling (NEW)
        'reg_alpha': 1.0,                  # L1 regularization (NEW)
        'reg_lambda': 2.0,                 # L2 regularization (NEW)
        'gamma': 0.1,                      # Min loss reduction for split (NEW)
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'random_state': 42,
        'tree_method': 'hist'
    }
    
    # Train with early stopping
    model = xgb.XGBClassifier(**params, early_stopping_rounds=20)
    
    # Fit with validation set for early stopping
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )
    
    # Predictions
    y_pred_train = model.predict(X_train)
    y_pred_val = model.predict(X_val)
    y_pred_test = model.predict(X_test)
    
    y_pred_proba_val = model.predict_proba(X_val)[:, 1]
    y_pred_proba_test = model.predict_proba(X_test)[:, 1]
    
    # Evaluation
    train_acc = accuracy_score(y_train, y_pred_train)
    val_acc = accuracy_score(y_val, y_pred_val)
    test_acc = accuracy_score(y_test, y_pred_test)
    
    # Calculate overfitting gap
    train_test_gap = train_acc - test_acc
    
    # ROC AUC
    try:
        roc_auc_val = roc_auc_score(y_val, y_pred_proba_val)
        roc_auc_test = roc_auc_score(y_test, y_pred_proba_test)
        
        print(f"\nPerformance Metrics:")
        print(f"Training Accuracy:   {train_acc:.1%}")
        print(f"Validation Accuracy: {val_acc:.1%}")
        print(f"Test Accuracy:       {test_acc:.1%}")
        print(f"Train-Test Gap:      {train_test_gap:.1%}")
        print(f"Validation ROC AUC:  {roc_auc_val:.4f}")
        print(f"Test ROC AUC:        {roc_auc_test:.4f}")
        print(f"Best Iteration:      {model.best_iteration}")
        
        # Overfitting warning
        if train_test_gap > 0.10:
            print(f"⚠️ WARNING: High train-test gap ({train_test_gap:.1%})")
        elif train_test_gap > 0.05:
            print(f"ℹ️ INFO: Mild train-test gap ({train_test_gap:.1%})")
        else:
            print(f"✓ GOOD: Low train-test gap ({train_test_gap:.1%})")
            
    except ValueError:
        roc_auc_val = None
        roc_auc_test = None
        print(f"\nPerformance Metrics:")
        print(f"Training Accuracy:   {train_acc:.1%}")
        print(f"Validation Accuracy: {val_acc:.1%}")
        print(f"Test Accuracy:       {test_acc:.1%}")
        print(f"Train-Test Gap:      {train_test_gap:.1%}")
        print(f"ROC AUC: N/A")
    
    # Classification report
    print(f"\nClassification Report (Test Set):")
    print(classification_report(y_test, y_pred_test, 
                                target_names=['Inactive', 'Active'], zero_division=0))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 5 Most Important Features:")
    for idx, row in feature_importance.head(5).iterrows():
        print(f"  {row['feature']:<20} {row['importance']:.4f}")
    
    return model, feature_importance, roc_auc_val, roc_auc_test, val_acc, test_acc, train_acc, train_test_gap


def main():
    
    print("="*80)
    print("NEUROFINANCE - ANTI-OVERFITTING XGBOOST (65/35 SPLIT)")
    print("="*80)
    
    # ========================================================================
    # 1. LOADING DATA
    # ========================================================================
    
    print("\n1. LOADING DATA...")
    print("-" * 80)
    
    df_pre = pd.read_csv('../nifty_bank_pre_covid.csv')
    df_post = pd.read_csv('../nifty_bank_post_covid.csv')
    
    print(f"Pre-COVID:  {len(df_pre)} rows")
    print(f"Post-COVID: {len(df_post)} rows")
    
    # ========================================================================
    # 2. ADD INSULA FEATURES
    # ========================================================================
    
    print("\n2. ADDING INSULA FEATURES...")
    print("-" * 80)
    
    df_pre = add_insula_features(df_pre)
    df_post = add_insula_features(df_post)
    
    print("✓ Added: gap_open, intraday_range, volume_spike")
    
    # ========================================================================
    # 3. PREPARE DATA SPLITS (65/35)
    # ========================================================================
    
    print("\n3. PREPARING DATA SPLITS (65/35)...")
    print("-" * 80)
    
    exclude_cols = ['date', 'dividends', 'stock_splits']
    feature_cols = [col for col in df_pre.columns if col not in exclude_cols]
    
    df_combined = pd.concat([df_pre, df_post], ignore_index=True)
    X_all = df_combined[feature_cols]
    
    # 65/35 split
    X_train_full, X_temp = train_test_split(X_all, test_size=0.35, random_state=42)
    # Split the 35% into validation and test (17.5% each)
    X_val, X_test = train_test_split(X_temp, test_size=0.50, random_state=42)
    
    print(f"Data split: Train={len(X_train_full)} (65%), Val={len(X_val)} (17.5%), Test={len(X_test)} (17.5%)")
    
    # ========================================================================
    # 4. CREATE ACTIVATION LABELS
    # ========================================================================
    
    print("\n4. CREATING BRAIN ACTIVATION LABELS (NO LEAKAGE)...")
    print("-" * 80)
    
    df_train_full = pd.DataFrame(X_train_full)
    df_train_full, activation_thresholds = create_activation_labels(df_train_full, thresholds_dict=None)
    
    df_val = pd.DataFrame(X_val)
    df_val, _ = create_activation_labels(df_val, thresholds_dict=activation_thresholds)
    
    df_test = pd.DataFrame(X_test)
    df_test, _ = create_activation_labels(df_test, thresholds_dict=activation_thresholds)
    
    # ========================================================================
    # 5. TRAIN OPTIMIZED MODELS
    # ========================================================================
    
    print("\n5. TRAINING ANTI-OVERFITTING XGBOOST MODELS...")
    print("="*80)
    
    exclude_cols = ['value_active', 'risk_active', 'sentiment_active', 'insula_active', 'control_active']
    feature_cols_final = [col for col in df_train_full.columns if col not in exclude_cols]
    
    models = {}
    importance_dict = {}
    results = {}
    
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        X_train = df_train_full[feature_cols_final]
        y_train = df_train_full[f'{system}_active']
        
        X_val_data = df_val[feature_cols_final]
        y_val = df_val[f'{system}_active']
        
        X_test_data = df_test[feature_cols_final]
        y_test = df_test[f'{system}_active']
        
        model, importance, roc_val, roc_test, val_acc, test_acc, train_acc, gap = train_brain_system_model_optimized(
            X_train, y_train, X_val_data, y_val, X_test_data, y_test, system
        )
        
        models[system] = model
        importance_dict[system] = importance
        results[system] = {
            'train_acc': train_acc,
            'val_acc': val_acc,
            'test_acc': test_acc,
            'roc_val': roc_val,
            'roc_test': roc_test,
            'overfitting_gap': gap
        }
    
    # ========================================================================
    # 6. SAVE RESULTS
    # ========================================================================
    
    print("\n6. SAVING RESULTS...")
    print("="*80)
    
    os.makedirs('Results_AntiOverfitting_65_35', exist_ok=True)
    
    # Performance comparison
    perf_data = []
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        res = results[system]
        perf_data.append({
            'System': system.title(),
            'Train_Accuracy_%': res['train_acc'] * 100,
            'Validation_Accuracy_%': res['val_acc'] * 100,
            'Test_Accuracy_%': res['test_acc'] * 100,
            'Train_Test_Gap_%': res['overfitting_gap'] * 100,
            'Validation_ROC_AUC': res['roc_val'] if res['roc_val'] else 'N/A',
            'Test_ROC_AUC': res['roc_test'] if res['roc_test'] else 'N/A'
        })
    
    perf_df = pd.DataFrame(perf_data)
    perf_df.to_csv('Results_AntiOverfitting_65_35/model_performance_optimized_65_35.csv', index=False)
    print("✓ Saved: Results_AntiOverfitting_65_35/model_performance_optimized_65_35.csv")
    
    # ========================================================================
    # 7. COMPARISON SUMMARY
    # ========================================================================
    
    print("\n" + "="*80)
    print("ANTI-OVERFITTING RESULTS (65/35 SPLIT)")
    print("="*80)
    
    print("\nMODEL PERFORMANCE (OPTIMIZED):")
    print("-" * 80)
    print(f"{'System':<12} {'Train':<8} {'Val':<8} {'Test':<8} {'Gap':<8} {'ROC AUC':<10}")
    print("-" * 80)
    
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        res = results[system]
        train = res['train_acc']
        val = res['val_acc']
        test = res['test_acc']
        gap = res['overfitting_gap']
        roc = res['roc_test']
        
        roc_str = f"{roc:.4f}" if roc is not None else "N/A"
        print(f"{system.title():<12} {train:>6.1%} {val:>6.1%} {test:>6.1%} {gap:>6.1%} {roc_str:>9}")
    
    # Calculate averages
    avg_gap = np.mean([results[s]['overfitting_gap'] for s in results.keys()])
    avg_test = np.mean([results[s]['test_acc'] for s in results.keys()])
    
    print("\n" + "-" * 80)
    print(f"Average Test Accuracy: {avg_test:.1%}")
    print(f"Average Train-Test Gap: {avg_gap:.1%}")
    
    print("\nOVERFITTING ASSESSMENT:")
    print("-" * 80)
    if avg_gap < 0.03:
        print("✅ EXCELLENT: Minimal overfitting (<3% gap)")
    elif avg_gap < 0.05:
        print("✅ GOOD: Low overfitting (3-5% gap)")
    elif avg_gap < 0.10:
        print("✓ ACCEPTABLE: Mild overfitting (5-10% gap)")
    else:
        print("⚠️ WARNING: Significant overfitting (>10% gap)")
    
    print("\nREGULARIZATION TECHNIQUES APPLIED:")
    print("-" * 80)
    print("✓ max_depth: 5 → 3 (shallower trees)")
    print("✓ learning_rate: 0.1 → 0.05 (slower learning)")
    print("✓ min_child_weight: 1 → 5 (conservative splits)")
    print("✓ subsample: 0.8 (row sampling)")
    print("✓ colsample_bytree: 0.8 (feature sampling)")
    print("✓ reg_alpha: 1.0 (L1 regularization)")
    print("✓ reg_lambda: 2.0 (L2 regularization)")
    print("✓ gamma: 0.1 (min loss reduction)")
    print("✓ early_stopping_rounds: 20")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
