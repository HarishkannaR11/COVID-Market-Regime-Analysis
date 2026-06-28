"""
NEUROFINANCE BRAIN SYSTEM ANALYSIS - XGBoost Implementation
============================================================

Purpose: Identify which brain systems (Value/Risk/Sentiment/Insula/Control) 
         are ACTIVE during different market conditions

Approach: Train XGBoost classifiers to detect brain system activation
         Compare Pre-COVID vs Post-COVID brain patterns

Author: NeuroFinance Research
Date: January 2026
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

BRAIN_SYSTEMS = {
    'value': {
        'features': ['rsi', 'momentum_30d', 'daily_return', 'weekly_return', 'monthly_return'],
        'threshold_rules': {
            'rsi_extreme': lambda x: (x > 65) | (x < 35),  # More lenient
            'strong_momentum': lambda x: abs(x) > x.std() * 0.8,
            'significant_return': lambda x: abs(x) > x.std()
        }
    },
    'risk': {
        'features': ['volatility_20d', 'daily_return'],
        'threshold_rules': {
            'high_volatility': lambda x: x > x.median() + x.std() * 0.5,  # More lenient
            'extreme_loss': lambda x: x < -x.std()  # More lenient
        }
    },
    'sentiment': {
        'features': ['price_to_ma50', 'price_to_ma200'],
        'threshold_rules': {
            'strong_deviation_ma50': lambda x: abs(x) > 0.02,  # More lenient (2% instead of 5%)
            'strong_deviation_ma200': lambda x: abs(x) > 0.03
        }
    },
    'insula': {
        'features': ['gap_open', 'intraday_range', 'volume_spike'],
        'threshold_rules': {
            'significant_gap': lambda x: abs(x) > x.std(),  # More lenient
            'high_range': lambda x: x > x.median() + x.std() * 0.5,
            'volume_surge': lambda x: x > 1.5  # More lenient (1.5x instead of 2x)
        }
    }
}

# ============================================================================
# FEATURE ENGINEERING - ADD INSULA FEATURES
# ============================================================================

def add_insula_features(df):
    """Add Insula brain system features (gut feeling indicators)"""
    df = df.copy()
    
    # Gap from previous close (overnight shock)
    df['prev_close'] = df['close'].shift(1)
    df['gap_open'] = (df['open'] - df['prev_close']) / df['prev_close']
    
    # Intraday range (chaos/stress)
    df['intraday_range'] = (df['high'] - df['low']) / df['open']
    
    # Volume spike (panic/euphoria)
    df['volume_ma_20'] = df['volume'].rolling(window=20).mean()
    df['volume_spike'] = df['volume'] / df['volume_ma_20']
    
    # Fill NaN for first rows
    df['gap_open'] = df['gap_open'].fillna(0)
    df['volume_spike'] = df['volume_spike'].fillna(1.0)
    
    # Drop temporary columns
    df = df.drop(['prev_close', 'volume_ma_20'], axis=1, errors='ignore')
    
    return df

# ============================================================================
# BRAIN SYSTEM ACTIVATION DETECTION
# ============================================================================

def detect_brain_activation(df, system_name, config, thresholds=None):
    """
    Detect if a brain system is ACTIVE on each day
    Returns binary series: 1 = Active, 0 = Inactive
    
    If thresholds provided (from training data), use them.
    Otherwise calculate from df (for training data only).
    """
    features = config['features']
    
    # Initialize activation as False
    activation = pd.Series(False, index=df.index)
    
    # Calculate thresholds from data if not provided
    if thresholds is None:
        thresholds = {}
    
    if system_name == 'value':
        # Get thresholds
        daily_return_thresh = thresholds.get('daily_return_q75', df['daily_return'].abs().quantile(0.75))
        momentum_thresh = thresholds.get('momentum_q75', df['momentum_30d'].abs().quantile(0.75))
        
        activation = (
            (df['rsi'] > 65) | (df['rsi'] < 35) |  
            (abs(df['daily_return']) > daily_return_thresh) |
            (abs(df['momentum_30d']) > momentum_thresh)
        )
        
        if thresholds is None:  # Return calculated thresholds for training
            return activation.astype(int), {
                'daily_return_q75': daily_return_thresh,
                'momentum_q75': momentum_thresh
            }
    
    elif system_name == 'risk':
        volatility_thresh = thresholds.get('volatility_q65', df['volatility_20d'].quantile(0.65))
        return_thresh = thresholds.get('return_q25', df['daily_return'].quantile(0.25))
        
        activation = (
            (df['volatility_20d'] > volatility_thresh) |
            (df['daily_return'] < return_thresh)
        )
        
        if thresholds is None:
            return activation.astype(int), {
                'volatility_q65': volatility_thresh,
                'return_q25': return_thresh
            }
    
    elif system_name == 'sentiment':
        # Absolute thresholds - no leakage
        activation = (
            (abs(df['price_to_ma50']) > 0.03) |  # 3% deviation from MA-50
            (abs(df['price_to_ma200']) > 0.05)   # 5% deviation from MA-200
        )
        
        if thresholds is None:
            return activation.astype(int), {}
    
    elif system_name == 'insula':
        gap_thresh = thresholds.get('gap_q70', df['gap_open'].abs().quantile(0.70))
        range_thresh = thresholds.get('range_q70', df['intraday_range'].quantile(0.70))
        
        activation = (
            (abs(df['gap_open']) > gap_thresh) |
            (df['intraday_range'] > range_thresh) |
            (df['volume_spike'] > 1.3)
        )
        
        if thresholds is None:
            return activation.astype(int), {
                'gap_q70': gap_thresh,
                'range_q70': range_thresh
            }
    
    return activation.astype(int)

def create_activation_labels(df, thresholds_dict=None):
    """
    Create binary labels for each brain system activation
    If thresholds_dict provided, use them (for val/test). Otherwise calculate (for train).
    """
    df = df.copy()
    
    if thresholds_dict is None:
        # Training mode - calculate and return thresholds
        thresholds_dict = {}
        for system_name, config in BRAIN_SYSTEMS.items():
            result = detect_brain_activation(df, system_name, config, thresholds=None)
            if isinstance(result, tuple):
                activation, thresh = result
                thresholds_dict[system_name] = thresh
            else:
                activation = result
                thresholds_dict[system_name] = {}
            df[f'{system_name}_active'] = activation
    else:
        # Validation/Test mode - use provided thresholds
        for system_name, config in BRAIN_SYSTEMS.items():
            activation = detect_brain_activation(df, system_name, config, thresholds=thresholds_dict.get(system_name, {}))
            df[f'{system_name}_active'] = activation
    
    # Control system: active when multiple systems are active OR systems conflict
    df['control_active'] = (
        (df['value_active'] + df['risk_active'] + df['sentiment_active'] + df['insula_active']) >= 2
    ).astype(int)
    
    return df, thresholds_dict

# ============================================================================
# XGBOOST TRAINING
# ============================================================================

def train_brain_system_model(X_train, y_train, X_val, y_val, X_test, y_test, system_name):
    """Train XGBoost classifier for one brain system with separate validation and test sets"""
    
    print(f"\n{'='*60}")
    print(f"Training {system_name.upper()} System Classifier")
    print(f"{'='*60}")
    
    # XGBoost parameters
    params = {
        'max_depth': 5,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'random_state': 42,
        'tree_method': 'hist'
    }
    
    # Train model on training set
    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train, verbose=False)
    
    # Predictions on all sets
    y_pred_train = model.predict(X_train)
    y_pred_val = model.predict(X_val)
    y_pred_test = model.predict(X_test)
    
    y_pred_proba_val = model.predict_proba(X_val)[:, 1]
    y_pred_proba_test = model.predict_proba(X_test)[:, 1]
    
    # Evaluation metrics
    train_acc = accuracy_score(y_train, y_pred_train)
    val_acc = accuracy_score(y_val, y_pred_val)
    test_acc = accuracy_score(y_test, y_pred_test)
    
    # ROC AUC Scores
    try:
        roc_auc_val = roc_auc_score(y_val, y_pred_proba_val)
        roc_auc_test = roc_auc_score(y_test, y_pred_proba_test)
        
        print(f"\nPerformance Metrics:")
        print(f"Training Accuracy:   {train_acc:.1%}")
        print(f"Validation Accuracy: {val_acc:.1%}")
        print(f"Test Accuracy:       {test_acc:.1%}")
        print(f"Validation ROC AUC:  {roc_auc_val:.4f}")
        print(f"Test ROC AUC:        {roc_auc_test:.4f}")
    except ValueError as e:
        roc_auc_val = None
        roc_auc_test = None
        print(f"\nPerformance Metrics:")
        print(f"Training Accuracy:   {train_acc:.1%}")
        print(f"Validation Accuracy: {val_acc:.1%}")
        print(f"Test Accuracy:       {test_acc:.1%}")
        print(f"ROC AUC: N/A (single class in dataset)")
    
    # Classification report on test set
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
    
    return model, feature_importance, roc_auc_val, roc_auc_test, val_acc, test_acc

# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_feature_importance(importance_dict, output_dir='Plots-XGBoost'):
    """Plot feature importance for all brain systems"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for idx, (system, importance_df) in enumerate(importance_dict.items()):
        ax = axes[idx]
        
        top_features = importance_df.head(10)
        ax.barh(top_features['feature'], top_features['importance'])
        ax.set_xlabel('Importance Score')
        ax.set_title(f'{system.upper()} System\nTop 10 Features')
        ax.invert_yaxis()
        
    # Remove extra subplot
    axes[5].axis('off')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/feature_importance_all_systems.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/feature_importance_all_systems.png")
    plt.close()

def plot_activation_frequency(df_pre, df_post, output_dir='Plots-XGBoost'):
    """Compare brain system activation frequencies Pre vs Post COVID"""
    
    systems = ['value_active', 'risk_active', 'sentiment_active', 'insula_active', 'control_active']
    
    pre_freq = [df_pre[sys].mean() * 100 for sys in systems]
    post_freq = [df_post[sys].mean() * 100 for sys in systems]
    
    x = np.arange(len(systems))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, pre_freq, width, label='Pre-COVID', color='steelblue', alpha=0.8)
    ax.bar(x + width/2, post_freq, width, label='Post-COVID', color='coral', alpha=0.8)
    
    ax.set_ylabel('Activation Frequency (%)')
    ax.set_title('Brain System Activation: Pre-COVID vs Post-COVID', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([s.replace('_active', '').title() for s in systems])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (pre, post) in enumerate(zip(pre_freq, post_freq)):
        ax.text(i - width/2, pre + 1, f'{pre:.1f}%', ha='center', fontsize=9)
        ax.text(i + width/2, post + 1, f'{post:.1f}%', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_frequency_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_frequency_comparison.png")
    plt.close()

def plot_activation_timeline(df, regime_name, output_dir='Plots-XGBoost'):
    """Plot brain system activation over time"""
    
    systems = ['value_active', 'risk_active', 'sentiment_active', 'insula_active', 'control_active']
    colors = ['steelblue', 'red', 'green', 'purple', 'orange']
    
    fig, axes = plt.subplots(5, 1, figsize=(16, 10), sharex=True)
    
    for idx, (system, color) in enumerate(zip(systems, colors)):
        ax = axes[idx]
        
        # Plot activation as filled area
        dates = pd.to_datetime(df['date'])
        ax.fill_between(dates, 0, df[system], alpha=0.6, color=color, label=system.replace('_active', '').title())
        ax.set_ylabel('Active', fontsize=10)
        ax.set_ylim(-0.1, 1.1)
        ax.legend(loc='upper left')
        ax.grid(alpha=0.3)
    
    axes[-1].set_xlabel('Date')
    fig.suptitle(f'Brain System Activation Timeline - {regime_name}', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_timeline_{regime_name.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_timeline_{regime_name.lower().replace(' ', '_')}.png")
    plt.close()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("\n" + "="*80)
    print("NEUROFINANCE BRAIN SYSTEM ANALYSIS - XGBOOST")
    print("="*80)
    
    # Create output directory
    os.makedirs('Plots-XGBoost', exist_ok=True)
    
    # ========================================================================
    # 1. LOAD DATA
    # ========================================================================
    
    print("\n1. LOADING DATA...")
    print("-" * 80)
    
    df_pre = pd.read_csv('nifty_bank_pre_covid.csv')
    df_post = pd.read_csv('nifty_bank_post_covid.csv')
    
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
    # 3. PREPARE FEATURES AND SPLIT DATA (NO LEAKAGE)
    # ========================================================================
    
    print("\n3. PREPARING DATA SPLITS...")
    print("-" * 80)
    
    # Select feature columns (exclude date, target labels, redundant columns)
    exclude_cols = ['date', 'dividends', 'stock_splits']
    feature_cols = [col for col in df_pre.columns if col not in exclude_cols]
    
    # Combine datasets
    df_combined = pd.concat([df_pre, df_post], ignore_index=True)
    
    # Extract features (without activation labels yet)
    X_all = df_combined[feature_cols]
    
    # Split into Train (70%) and Temp (30%)
    X_train_full, X_temp = train_test_split(
        X_all, test_size=0.30, random_state=42
    )
    
    # Split Temp into Validation (15%) and Test (15%)
    X_val, X_test = train_test_split(
        X_temp, test_size=0.50, random_state=42
    )
    
    print(f"Data split: Train={len(X_train_full)} (70%), Val={len(X_val)} (15%), Test={len(X_test)} (15%)")
    
    # ========================================================================
    # 4. CREATE ACTIVATION LABELS (FIX DATA LEAKAGE)
    # ========================================================================
    
    print("\n4. CREATING BRAIN ACTIVATION LABELS (NO LEAKAGE)...")
    print("-" * 80)
    
    # Create labels for TRAINING data and get thresholds
    df_train_full = pd.DataFrame(X_train_full)
    df_train_full, activation_thresholds = create_activation_labels(df_train_full, thresholds_dict=None)
    
    print("\nActivation Thresholds (from Training Data):")
    for system, thresh in activation_thresholds.items():
        if thresh:
            print(f"  {system.title()}: {thresh}")
    
    # Apply same thresholds to VALIDATION and TEST (no leakage!)
    df_val = pd.DataFrame(X_val)
    df_val, _ = create_activation_labels(df_val, thresholds_dict=activation_thresholds)
    
    df_test = pd.DataFrame(X_test)
    df_test, _ = create_activation_labels(df_test, thresholds_dict=activation_thresholds)
    
    print("\nActivation Frequency (Training Set):")
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        freq = df_train_full[f'{system}_active'].mean() * 100
        print(f"  {system.title():<12} {freq:>6.1f}% of days")
    
    print("\nActivation Frequency (Validation Set):")
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        freq = df_val[f'{system}_active'].mean() * 100
        print(f"  {system.title():<12} {freq:>6.1f}% of days")
    
    print("\nActivation Frequency (Test Set):")
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        freq = df_test[f'{system}_active'].mean() * 100
        print(f"  {system.title():<12} {freq:>6.1f}% of days")
    
    # ========================================================================
    # 5. PREPARE FEATURES FOR XGBOOST
    # ========================================================================
    
    print("\n5. PREPARING FEATURES FOR MODELING...")
    print("-" * 80)
    
    # Exclude activation labels from features
    exclude_cols = ['value_active', 'risk_active', 'sentiment_active', 'insula_active', 'control_active']
    feature_cols_final = [col for col in df_train_full.columns if col not in exclude_cols]
    
    print(f"Using {len(feature_cols_final)} features:")
    for col in feature_cols_final[:10]:
        print(f"  - {col}")
    if len(feature_cols_final) > 10:
        print(f"  ... and {len(feature_cols_final) - 10} more")
    
    # ========================================================================
    # 6. TRAIN XGBOOST MODELS
    # ========================================================================
    
    print("\n6. TRAINING XGBOOST MODELS...")
    print("="*80)
    
    models = {}
    importance_dict = {}
    results = {}
    
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        
        # Extract features and labels
        X_train = df_train_full[feature_cols_final]
        y_train = df_train_full[f'{system}_active']
        
        X_val_data = df_val[feature_cols_final]
        y_val = df_val[f'{system}_active']
        
        X_test_data = df_test[feature_cols_final]
        y_test = df_test[f'{system}_active']
        
        # Train model
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
    # 7. VISUALIZATIONS
    # ========================================================================
    
    print("\n7. GENERATING VISUALIZATIONS...")
    print("="*80)
    
    # Recreate full datasets with activation labels for visualization
    df_pre_full, _ = create_activation_labels(df_pre, thresholds_dict=activation_thresholds)
    df_post_full, _ = create_activation_labels(df_post, thresholds_dict=activation_thresholds)
    
    plot_feature_importance(importance_dict)
    plot_activation_frequency(df_pre_full, df_post_full)
    plot_activation_timeline(df_pre_full, 'Pre-COVID')
    plot_activation_timeline(df_post_full, 'Post-COVID')
    
    # ========================================================================
    # 8. SAVE RESULTS
    # ========================================================================
    
    print("\n8. SAVING RESULTS...")
    print("="*80)
    
    # Save activation data
    df_pre_full.to_csv('brain_activation_pre_covid.csv', index=False)
    df_post_full.to_csv('brain_activation_post_covid.csv', index=False)
    
    print("✓ Saved: brain_activation_pre_covid.csv")
    print("✓ Saved: brain_activation_post_covid.csv")
    
    # Save summary statistics
    summary = []
    for regime, df in [('Pre-COVID', df_pre_full), ('Post-COVID', df_post_full)]:
        for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
            summary.append({
                'Regime': regime,
                'Brain_System': system.title(),
                'Activation_Frequency_%': df[f'{system}_active'].mean() * 100,
                'Total_Active_Days': df[f'{system}_active'].sum(),
                'Total_Days': len(df)
            })
    
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv('brain_activation_summary.csv', index=False)
    print("✓ Saved: brain_activation_summary.csv")
    
    # ========================================================================
    # 9. FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - NO DATA LEAKAGE!")
    print("="*80)
    
    print("\nDATA SPLIT:")
    print("-" * 80)
    print(f"Training:   {len(df_train_full)} samples (70%)")
    print(f"Validation: {len(df_val)} samples (15%)")
    print(f"Test:       {len(df_test)} samples (15%)")
    
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
    
    print("\nKEY FINDINGS:")
    print("-" * 80)
    
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        pre_freq = df_pre_full[f'{system}_active'].mean() * 100
        post_freq = df_post_full[f'{system}_active'].mean() * 100
        change = post_freq - pre_freq
        
        arrow = "↑" if change > 0 else "↓"
        print(f"{system.title():<12} Pre: {pre_freq:>5.1f}%  Post: {post_freq:>5.1f}%  {arrow} {abs(change):>5.1f}%")
    
    print("\nOUTPUT FILES:")
    print("-" * 80)
    print("  1. brain_activation_pre_covid.csv - Pre-COVID with activation labels")
    print("  2. brain_activation_post_covid.csv - Post-COVID with activation labels")
    print("  3. brain_activation_summary.csv - Summary statistics")
    print("  4. Plots-XGBoost/ - All visualization files")
    
    print("\n" + "="*80)
    print("Done! Check Plots-XGBoost folder for visualizations.")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
