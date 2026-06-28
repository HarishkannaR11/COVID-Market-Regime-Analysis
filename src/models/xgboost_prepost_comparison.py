"""
ANTI-OVERFITTING XGBOOST WITH PRE vs POST COVID COMPARISON
===========================================================

This script:
1. Trains optimized XGBoost models (70/15/15 split)
2. Applies models to Pre-COVID and Post-COVID data separately
3. Compares brain activation frequencies between periods
4. Generates comprehensive comparison plots
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

# Add parent directories to path
sys.path.append('..')
sys.path.append('../..')
from xgboost_brain_analysis import (
    BRAIN_SYSTEMS, add_insula_features, detect_brain_activation, 
    create_activation_labels, plot_feature_importance
)

def train_brain_system_model_optimized(X_train, y_train, X_val, y_val, X_test, y_test, system_name):
    """Train XGBoost with anti-overfitting measures"""
    
    print(f"\n{'='*60}")
    print(f"Training {system_name.upper()} System (Anti-Overfitting)")
    print(f"{'='*60}")
    
    params = {
        'max_depth': 3,
        'learning_rate': 0.05,
        'n_estimators': 200,
        'min_child_weight': 5,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'reg_alpha': 1.0,
        'reg_lambda': 2.0,
        'gamma': 0.1,
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'random_state': 42,
        'tree_method': 'hist'
    }
    
    model = xgb.XGBClassifier(**params, early_stopping_rounds=20)
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    
    # Predictions
    y_pred_test = model.predict(X_test)
    y_pred_proba_test = model.predict_proba(X_test)[:, 1]
    
    test_acc = accuracy_score(y_test, y_pred_test)
    
    try:
        roc_auc_test = roc_auc_score(y_test, y_pred_proba_test)
        print(f"Test Accuracy: {test_acc:.1%} | ROC AUC: {roc_auc_test:.4f}")
    except ValueError:
        roc_auc_test = None
        print(f"Test Accuracy: {test_acc:.1%}")
    
    return model


def predict_activations(models, df, feature_cols):
    """Apply trained models to predict activations"""
    predictions = {}
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        X = df[feature_cols]
        predictions[f'{system}_active'] = models[system].predict(X)
    return pd.DataFrame(predictions)


def create_comparison_plots(df_pre_activations, df_post_activations, df_pre, df_post, output_dir):
    """Create comprehensive comparison plots"""
    
    print("\nGenerating comparison plots...")
    
    # Calculate activation frequencies
    systems = ['value', 'risk', 'sentiment', 'insula', 'control']
    pre_freq = {}
    post_freq = {}
    
    for system in systems:
        pre_freq[system] = df_pre_activations[f'{system}_active'].mean() * 100
        post_freq[system] = df_post_activations[f'{system}_active'].mean() * 100
    
    # 1. BAR CHART: Activation Frequency Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(systems))
    width = 0.35
    
    pre_values = [pre_freq[s] for s in systems]
    post_values = [post_freq[s] for s in systems]
    
    bars1 = ax.bar(x - width/2, pre_values, width, label='Pre-COVID', color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, post_values, width, label='Post-COVID', color='#e74c3c', alpha=0.8)
    
    ax.set_xlabel('Brain System', fontsize=12, fontweight='bold')
    ax.set_ylabel('Activation Frequency (%)', fontsize=12, fontweight='bold')
    ax.set_title('Brain System Activation: Pre-COVID vs Post-COVID\n(Anti-Overfitting Models)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([s.title() for s in systems])
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 100)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_frequency_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_frequency_comparison.png")
    plt.close()
    
    # 2. CHANGE ANALYSIS
    fig, ax = plt.subplots(figsize=(12, 6))
    changes = [post_freq[s] - pre_freq[s] for s in systems]
    colors = ['#27ae60' if c > 0 else '#e74c3c' for c in changes]
    
    bars = ax.barh(range(len(systems)), changes, color=colors, alpha=0.7)
    ax.set_yticks(range(len(systems)))
    ax.set_yticklabels([s.title() for s in systems])
    ax.set_xlabel('Change in Activation Frequency (percentage points)', fontsize=12, fontweight='bold')
    ax.set_title('Brain System Activation Changes: Pre → Post COVID\n(Anti-Overfitting Models)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, change) in enumerate(zip(bars, changes)):
        x_pos = change + (1 if change > 0 else -1)
        ax.text(x_pos, i, f'{change:+.1f}pp', va='center', 
               ha='left' if change > 0 else 'right', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_change_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_change_analysis.png")
    plt.close()
    
    # 3. HEATMAP: Activation Patterns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
    
    # Pre-COVID heatmap
    pre_matrix = df_pre_activations[[f'{s}_active' for s in systems]].T
    sns.heatmap(pre_matrix, cmap='YlOrRd', cbar_kws={'label': 'Active (1) / Inactive (0)'}, 
                ax=ax1, yticklabels=[s.title() for s in systems], xticklabels=False)
    ax1.set_title('Pre-COVID Activation Patterns', fontsize=12, fontweight='bold', pad=15)
    ax1.set_xlabel('Trading Days', fontsize=10)
    
    # Post-COVID heatmap
    post_matrix = df_post_activations[[f'{s}_active' for s in systems]].T
    sns.heatmap(post_matrix, cmap='YlOrRd', cbar_kws={'label': 'Active (1) / Inactive (0)'}, 
                ax=ax2, yticklabels=[s.title() for s in systems], xticklabels=False)
    ax2.set_title('Post-COVID Activation Patterns', fontsize=12, fontweight='bold', pad=15)
    ax2.set_xlabel('Trading Days', fontsize=10)
    
    plt.suptitle('Brain System Activation Heatmaps\n(Anti-Overfitting Models)', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_heatmaps.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_heatmaps.png")
    plt.close()
    
    # 4. CORRELATION MATRIX
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Pre-COVID correlations
    pre_corr = df_pre_activations[[f'{s}_active' for s in systems]].corr()
    pre_corr.columns = [s.title() for s in systems]
    pre_corr.index = [s.title() for s in systems]
    sns.heatmap(pre_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                vmin=-1, vmax=1, ax=ax1, square=True)
    ax1.set_title('Pre-COVID System Correlations', fontsize=12, fontweight='bold')
    
    # Post-COVID correlations
    post_corr = df_post_activations[[f'{s}_active' for s in systems]].corr()
    post_corr.columns = [s.title() for s in systems]
    post_corr.index = [s.title() for s in systems]
    sns.heatmap(post_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                vmin=-1, vmax=1, ax=ax2, square=True)
    ax2.set_title('Post-COVID System Correlations', fontsize=12, fontweight='bold')
    
    plt.suptitle('Brain System Correlation Analysis\n(Anti-Overfitting Models)', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_correlations.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_correlations.png")
    plt.close()
    
    # 5. TIME SERIES LINE PLOTS - Individual Systems
    fig, axes = plt.subplots(5, 1, figsize=(16, 14))
    
    # Add dates for x-axis
    df_pre_with_dates = df_pre_activations.copy()
    df_pre_with_dates['date'] = pd.to_datetime(df_pre['date'].values)
    
    df_post_with_dates = df_post_activations.copy()
    df_post_with_dates['date'] = pd.to_datetime(df_post['date'].values)
    
    # Calculate rolling activation frequency (30-day window)
    for idx, system in enumerate(systems):
        ax = axes[idx]
        
        # Pre-COVID rolling activation
        pre_rolling = df_pre_with_dates.set_index('date')[f'{system}_active'].rolling(30, min_periods=1).mean() * 100
        post_rolling = df_post_with_dates.set_index('date')[f'{system}_active'].rolling(30, min_periods=1).mean() * 100
        
        # Plot Pre-COVID
        ax.plot(pre_rolling.index, pre_rolling.values, color='#3498db', linewidth=2, 
                label='Pre-COVID', alpha=0.8)
        ax.fill_between(pre_rolling.index, 0, pre_rolling.values, color='#3498db', alpha=0.2)
        
        # Plot Post-COVID  
        ax.plot(post_rolling.index, post_rolling.values, color='#e74c3c', linewidth=2, 
                label='Post-COVID', alpha=0.8)
        ax.fill_between(post_rolling.index, 0, post_rolling.values, color='#e74c3c', alpha=0.2)
        
        ax.set_ylabel('Activation %', fontsize=10, fontweight='bold')
        ax.set_title(f'{system.title()} System Activation (30-Day Rolling Average)', 
                     fontsize=11, fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(0, 100)
        ax.legend(loc='upper left', fontsize=9)
        
        # Add average lines
        ax.axhline(y=pre_freq[system], color='#3498db', linestyle='--', alpha=0.5, linewidth=1)
        ax.axhline(y=post_freq[system], color='#e74c3c', linestyle='--', alpha=0.5, linewidth=1)
    
    plt.suptitle('Brain System Activation Time Series\n(Anti-Overfitting Models)', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_timeseries_individual.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_timeseries_individual.png")
    plt.close()
    
    # 6. TIME SERIES LINE PLOTS - Combined Overlay
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
    
    colors = {'value': '#e74c3c', 'risk': '#f39c12', 'sentiment': '#27ae60', 
              'insula': '#9b59b6', 'control': '#3498db'}
    
    ts_labels = {'value': 'Value', 'risk': 'Risk', 'sentiment': 'Sentiment',
                 'insula': 'Anomaly Detection', 'control': 'Control'}

    # Pre-COVID
    for system in systems:
        pre_rolling = df_pre_with_dates.set_index('date')[f'{system}_active'].rolling(30, min_periods=1).mean() * 100
        ax1.plot(pre_rolling.index, pre_rolling.values, color=colors[system], 
                linewidth=2.5, label=ts_labels[system], alpha=0.8)
    
    ax1.set_ylabel('Activation Frequency (%)', fontsize=18, fontweight='bold')
    ax1.set_title('Pre-COVID: Brain System Activation Over Time (30-Day Rolling)', 
                  fontsize=20, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='both', labelsize=15)
    ax1.get_legend().remove() if ax1.get_legend() else None
    ax1.set_ylim(0, 100)
    
    # Post-COVID
    for system in systems:
        post_rolling = df_post_with_dates.set_index('date')[f'{system}_active'].rolling(30, min_periods=1).mean() * 100
        ax2.plot(post_rolling.index, post_rolling.values, color=colors[system], 
                linewidth=2.5, label=ts_labels[system], alpha=0.8)
    
    ax2.set_xlabel('Date', fontsize=18, fontweight='bold')
    ax2.set_ylabel('Activation Frequency (%)', fontsize=18, fontweight='bold')
    ax2.set_title('Post-COVID: Brain System Activation Over Time (30-Day Rolling)', 
                  fontsize=20, fontweight='bold', pad=15)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.tick_params(axis='both', labelsize=15)
    leg2 = ax2.legend(loc='lower left', fontsize=17, framealpha=1.0,
                      edgecolor='black', fancybox=True, shadow=False,
                      borderpad=0.9, handlelength=2.0, handletextpad=0.7,
                      labelspacing=0.6, markerscale=1.5)
    leg2.get_frame().set_linewidth(2.0)
    leg2.get_frame().set_facecolor('#EAF4FB')
    ax2.set_ylim(0, 100)
    
    plt.suptitle('Brain System Activation Trends: Pre vs Post COVID\n(Anti-Overfitting Models)', 
                 fontsize=24, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_timeseries_combined.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_timeseries_combined.png")
    plt.close()
    
    # 7. CUMULATIVE ACTIVATION LINE PLOT
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    label_names = {'value': 'Value', 'risk': 'Risk', 'sentiment': 'Sentiment',
                   'insula': 'Anomaly Detection', 'control': 'Control'}
    
    # Pre-COVID cumulative
    for system in systems:
        cumulative = df_pre_with_dates.set_index('date')[f'{system}_active'].cumsum()
        axes[0].plot(cumulative.index, cumulative.values, color=colors[system], 
                    linewidth=2.5, label=label_names[system], alpha=0.8)
    
    axes[0].set_ylabel('Cumulative Activations', fontsize=18, fontweight='bold')
    axes[0].set_title('Pre-COVID: Cumulative Brain System Activations', 
                     fontsize=20, fontweight='bold', pad=15)
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].tick_params(axis='both', labelsize=15)
    leg0 = axes[0].legend(loc='upper left', fontsize=18, framealpha=1.0,
                          edgecolor='black', fancybox=True, shadow=False,
                          borderpad=1.0, handlelength=3.5, handletextpad=1.0,
                          labelspacing=0.5, markerscale=1.5)
    leg0.get_frame().set_linewidth(1.8)
    leg0.get_frame().set_facecolor('#EAF4FB')
    
    # Post-COVID cumulative
    for system in systems:
        cumulative = df_post_with_dates.set_index('date')[f'{system}_active'].cumsum()
        axes[1].plot(cumulative.index, cumulative.values, color=colors[system], 
                    linewidth=2.5, label=label_names[system], alpha=0.8)
    
    axes[1].set_xlabel('Date', fontsize=18, fontweight='bold')
    axes[1].set_ylabel('Cumulative Activations', fontsize=18, fontweight='bold')
    axes[1].set_title('Post-COVID: Cumulative Brain System Activations', 
                     fontsize=20, fontweight='bold', pad=15)
    axes[1].grid(True, alpha=0.3, linestyle='--')
    axes[1].tick_params(axis='both', labelsize=15)
    leg1c = axes[1].legend(loc='upper left', fontsize=18, framealpha=1.0,
                           edgecolor='black', fancybox=True, shadow=False,
                           borderpad=1.0, handlelength=3.5, handletextpad=1.0,
                           labelspacing=0.5, markerscale=1.5)
    leg1c.get_frame().set_linewidth(1.8)
    leg1c.get_frame().set_facecolor('#EAF4FB')
    
    plt.suptitle('Cumulative Brain System Activations: Pre vs Post COVID\n(Anti-Overfitting Models)', 
                 fontsize=24, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activation_cumulative.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/activation_cumulative.png")
    plt.close()
    
    return pre_freq, post_freq, changes


def main():
    
    print("="*80)
    print("ANTI-OVERFITTING XGBOOST: PRE vs POST COVID ANALYSIS")
    print("="*80)
    
    # Create output directory
    output_dir = 'Results_PrePost_Comparison'
    os.makedirs(output_dir, exist_ok=True)
    
    # ========================================================================
    # 1. LOAD DATA
    # ========================================================================
    
    print("\n1. LOADING DATA...")
    print("-" * 80)
    
    df_pre = pd.read_csv('../../nifty_bank_pre_covid.csv')
    df_post = pd.read_csv('../../nifty_bank_post_covid.csv')
    
    print(f"Pre-COVID:  {len(df_pre)} rows (Jan 2017 - Feb 2020)")
    print(f"Post-COVID: {len(df_post)} rows (Mar 2020 - Feb 2023)")
    
    # ========================================================================
    # 2. ADD INSULA FEATURES
    # ========================================================================
    
    print("\n2. ADDING INSULA FEATURES...")
    print("-" * 80)
    
    df_pre = add_insula_features(df_pre)
    df_post = add_insula_features(df_post)
    
    print("✓ Added: gap_open, intraday_range, volume_spike")
    
    # ========================================================================
    # 3. PREPARE DATA SPLITS (70/15/15)
    # ========================================================================
    
    print("\n3. PREPARING DATA SPLITS (70/15/15)...")
    print("-" * 80)
    
    exclude_cols = ['date', 'dividends', 'stock_splits']
    feature_cols = [col for col in df_pre.columns if col not in exclude_cols]
    
    df_combined = pd.concat([df_pre, df_post], ignore_index=True)
    X_all = df_combined[feature_cols]
    
    X_train_full, X_temp = train_test_split(X_all, test_size=0.30, random_state=42)
    X_val, X_test = train_test_split(X_temp, test_size=0.50, random_state=42)
    
    print(f"Combined training: Train={len(X_train_full)} (70%), Val={len(X_val)} (15%), Test={len(X_test)} (15%)")
    
    # ========================================================================
    # 4. CREATE ACTIVATION LABELS (NO LEAKAGE)
    # ========================================================================
    
    print("\n4. CREATING BRAIN ACTIVATION LABELS (NO LEAKAGE)...")
    print("-" * 80)
    
    df_train_full = pd.DataFrame(X_train_full)
    df_train_full, activation_thresholds = create_activation_labels(df_train_full, thresholds_dict=None)
    
    df_val = pd.DataFrame(X_val)
    df_val, _ = create_activation_labels(df_val, thresholds_dict=activation_thresholds)
    
    df_test = pd.DataFrame(X_test)
    df_test, _ = create_activation_labels(df_test, thresholds_dict=activation_thresholds)
    
    print("✓ Thresholds calculated from training data only")
    
    # ========================================================================
    # 5. TRAIN OPTIMIZED MODELS
    # ========================================================================
    
    print("\n5. TRAINING ANTI-OVERFITTING XGBOOST MODELS...")
    print("="*80)
    
    exclude_activation_cols = ['value_active', 'risk_active', 'sentiment_active', 'insula_active', 'control_active']
    feature_cols_final = [col for col in df_train_full.columns if col not in exclude_activation_cols]
    
    models = {}
    
    for system in ['value', 'risk', 'sentiment', 'insula', 'control']:
        X_train = df_train_full[feature_cols_final]
        y_train = df_train_full[f'{system}_active']
        
        X_val_data = df_val[feature_cols_final]
        y_val = df_val[f'{system}_active']
        
        X_test_data = df_test[feature_cols_final]
        y_test = df_test[f'{system}_active']
        
        model = train_brain_system_model_optimized(
            X_train, y_train, X_val_data, y_val, X_test_data, y_test, system
        )
        
        models[system] = model
    
    # ========================================================================
    # 6. APPLY MODELS TO PRE/POST PERIODS
    # ========================================================================
    
    print("\n6. APPLYING MODELS TO PRE-COVID AND POST-COVID DATA...")
    print("="*80)
    
    # Prepare Pre-COVID data
    df_pre_features = df_pre[feature_cols]
    df_pre_activations = predict_activations(models, df_pre_features, feature_cols_final)
    
    # Prepare Post-COVID data
    df_post_features = df_post[feature_cols]
    df_post_activations = predict_activations(models, df_post_features, feature_cols_final)
    
    print(f"✓ Predictions generated for {len(df_pre_activations)} Pre-COVID days")
    print(f"✓ Predictions generated for {len(df_post_activations)} Post-COVID days")
    
    # ========================================================================
    # 7. GENERATE COMPARISON PLOTS
    # ========================================================================
    
    print("\n7. GENERATING COMPARISON PLOTS...")
    print("="*80)
    
    pre_freq, post_freq, changes = create_comparison_plots(
        df_pre_activations, df_post_activations, df_pre, df_post, output_dir
    )
    
    # ========================================================================
    # 8. SAVE COMPARISON STATISTICS
    # ========================================================================
    
    print("\n8. SAVING COMPARISON STATISTICS...")
    print("-" * 80)
    
    systems = ['value', 'risk', 'sentiment', 'insula', 'control']
    comparison_data = []
    
    for system in systems:
        comparison_data.append({
            'System': system.title(),
            'Pre_COVID_Frequency_%': pre_freq[system],
            'Post_COVID_Frequency_%': post_freq[system],
            'Change_pp': post_freq[system] - pre_freq[system],
            'Change_%': ((post_freq[system] - pre_freq[system]) / pre_freq[system] * 100) if pre_freq[system] > 0 else 0
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv(f'{output_dir}/activation_frequency_comparison.csv', index=False)
    print(f"✓ Saved: {output_dir}/activation_frequency_comparison.csv")
    
    # Save detailed activations
    df_pre_activations.to_csv(f'{output_dir}/pre_covid_activations.csv', index=False)
    df_post_activations.to_csv(f'{output_dir}/post_covid_activations.csv', index=False)
    print(f"✓ Saved: {output_dir}/pre_covid_activations.csv")
    print(f"✓ Saved: {output_dir}/post_covid_activations.csv")
    
    # ========================================================================
    # 9. DISPLAY SUMMARY
    # ========================================================================
    
    print("\n" + "="*80)
    print("PRE vs POST COVID COMPARISON SUMMARY")
    print("="*80)
    
    print("\nACTIVATION FREQUENCY COMPARISON:")
    print("-" * 80)
    print(f"{'System':<12} {'Pre-COVID':<12} {'Post-COVID':<12} {'Change':<12} {'% Change':<12}")
    print("-" * 80)
    
    for system in systems:
        pre = pre_freq[system]
        post = post_freq[system]
        change = post - pre
        pct_change = (change / pre * 100) if pre > 0 else 0
        
        change_str = f"+{change:.1f}pp" if change > 0 else f"{change:.1f}pp"
        pct_str = f"+{pct_change:.1f}%" if pct_change > 0 else f"{pct_change:.1f}%"
        
        print(f"{system.title():<12} {pre:>10.1f}% {post:>10.1f}% {change_str:>10} {pct_str:>10}")
    
    print("\nKEY INSIGHTS:")
    print("-" * 80)
    
    # Find biggest increase/decrease
    max_increase_system = max(systems, key=lambda s: post_freq[s] - pre_freq[s])
    max_decrease_system = min(systems, key=lambda s: post_freq[s] - pre_freq[s])
    
    max_increase = post_freq[max_increase_system] - pre_freq[max_increase_system]
    max_decrease = post_freq[max_decrease_system] - pre_freq[max_decrease_system]
    
    if max_increase > 0:
        print(f"✓ Biggest increase: {max_increase_system.title()} (+{max_increase:.1f}pp)")
    if max_decrease < 0:
        print(f"✓ Biggest decrease: {max_decrease_system.title()} ({max_decrease:.1f}pp)")
    
    print(f"\n✓ All results saved to: {output_dir}/")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
