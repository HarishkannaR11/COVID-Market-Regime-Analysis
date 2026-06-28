"""
NEUROFINANCE BRAIN SYSTEM ANALYSIS - 60/40 SPLIT
================================================

Train: 60% | Validation: 20% (50% of 40%) | Test: 20% (50% of 40%)
No data leakage - thresholds calculated only from training data
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

# Add parent directory to path to import functions
sys.path.append('..')
from xgboost_brain_analysis import (
    BRAIN_SYSTEMS, add_insula_features, detect_brain_activation, 
    create_activation_labels, train_brain_system_model,
    plot_feature_importance, plot_activation_frequency, plot_activation_timeline
)

def main():
    
    print("="*80)
    print("NEUROFINANCE BRAIN SYSTEM ANALYSIS - 60/40 SPLIT")
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
    # 3. PREPARE FEATURES AND SPLIT DATA (60/40 - NO LEAKAGE)
    # ========================================================================
    
    print("\n3. PREPARING DATA SPLITS (60/40)...")
    print("-" * 80)
    
    # Select feature columns
    exclude_cols = ['date', 'dividends', 'stock_splits']
    feature_cols = [col for col in df_pre.columns if col not in exclude_cols]
    
    # Combine datasets
    df_combined = pd.concat([df_pre, df_post], ignore_index=True)
    X_all = df_combined[feature_cols]
    
    # Split into Train (60%) and Temp (40%)
    X_train_full, X_temp = train_test_split(X_all, test_size=0.40, random_state=42)
    
    # Split Temp into Validation (20%) and Test (20%)
    X_val, X_test = train_test_split(X_temp, test_size=0.50, random_state=42)
    
    print(f"Data split: Train={len(X_train_full)} (60%), Val={len(X_val)} (20%), Test={len(X_test)} (20%)")
    
    # ========================================================================
    # 4. CREATE ACTIVATION LABELS (FIX DATA LEAKAGE)
    # ========================================================================
    
    print("\n4. CREATING BRAIN ACTIVATION LABELS (NO LEAKAGE)...")
    print("-" * 80)
    
    # Training data - calculate thresholds
    df_train_full = pd.DataFrame(X_train_full)
    df_train_full, activation_thresholds = create_activation_labels(df_train_full, thresholds_dict=None)
    
    # Validation data - use training thresholds
    df_val = pd.DataFrame(X_val)
    df_val, _ = create_activation_labels(df_val, thresholds_dict=activation_thresholds)
    
    # Test data - use training thresholds
    df_test = pd.DataFrame(X_test)
    df_test, _ = create_activation_labels(df_test, thresholds_dict=activation_thresholds)
    
    print("\nActivation Frequency (Training Set):")
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        freq = df_train_full[f'{system}_active'].mean() * 100
        print(f"  {system.title():<12} {freq:>6.1f}% of days")
    
    # ========================================================================
    # 5. TRAIN XGBOOST MODELS
    # ========================================================================
    
    print("\n5. TRAINING XGBOOST MODELS...")
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
        
        model, importance, roc_val, roc_test, val_acc, test_acc = train_brain_system_model(
            X_train, y_train, X_val_data, y_val, X_test_data, y_test, system
        )
        
        models[system] = model
        importance_dict[system] = importance
        results[system] = {
            'val_acc': val_acc,
            'test_acc': test_acc,
            'roc_val': roc_val,
            'roc_test': roc_test
        }
    
    # ========================================================================
    # 6. SAVE RESULTS
    # ========================================================================
    
    print("\n6. SAVING RESULTS...")
    print("="*80)
    
    # Create output directory
    os.makedirs('Results_60_40', exist_ok=True)
    
    # Save model performance
    perf_data = []
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        res = results[system]
        perf_data.append({
            'System': system.title(),
            'Validation_Accuracy_%': res['val_acc'] * 100,
            'Test_Accuracy_%': res['test_acc'] * 100,
            'Validation_ROC_AUC': res['roc_val'] if res['roc_val'] else 'N/A',
            'Test_ROC_AUC': res['roc_test'] if res['roc_test'] else 'N/A'
        })
    
    perf_df = pd.DataFrame(perf_data)
    perf_df.to_csv('Results_60_40/model_performance_60_40.csv', index=False)
    print("✓ Saved: Results_60_40/model_performance_60_40.csv")
    
    # Save data split info
    split_info = {
        'Split_Type': '60/40',
        'Train_Samples': len(df_train_full),
        'Train_Percentage': 60.0,
        'Validation_Samples': len(df_val),
        'Validation_Percentage': 20.0,
        'Test_Samples': len(df_test),
        'Test_Percentage': 20.0,
        'Total_Samples': len(df_combined),
        'Random_State': 42
    }
    
    split_df = pd.DataFrame([split_info])
    split_df.to_csv('Results_60_40/split_information_60_40.csv', index=False)
    print("✓ Saved: Results_60_40/split_information_60_40.csv")
    
    # ========================================================================
    # 7. FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - 60/40 SPLIT")
    print("="*80)
    
    print("\nDATA SPLIT:")
    print("-" * 80)
    print(f"Training:   {len(df_train_full)} samples (60.0%)")
    print(f"Validation: {len(df_val)} samples (20.0%)")
    print(f"Test:       {len(df_test)} samples (20.0%)")
    
    print("\nMODEL PERFORMANCE SUMMARY:")
    print("-" * 80)
    print(f"{'System':<12} {'Val Accuracy':<15} {'Test Accuracy':<15} {'Val ROC AUC':<12} {'Test ROC AUC':<12}")
    print("-" * 80)
    
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        res = results[system]
        val_acc = res['val_acc']
        test_acc = res['test_acc']
        roc_val = res['roc_val']
        roc_test = res['roc_test']
        
        roc_val_str = f"{roc_val:.4f}" if roc_val is not None else "N/A"
        roc_test_str = f"{roc_test:.4f}" if roc_test is not None else "N/A"
        
        print(f"{system.title():<12} {val_acc:>13.1%}  {test_acc:>13.1%}  {roc_val_str:>11}  {roc_test_str:>11}")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
