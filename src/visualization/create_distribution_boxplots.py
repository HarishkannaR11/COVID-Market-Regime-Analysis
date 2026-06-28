"""
Distribution and Box Plot Visualizations for XGBoost Brain Activation Analysis
Creates comprehensive distribution and box plots for features, activations, and model performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

# Create output directory
output_dir = Path('Plots-XGBoost')
output_dir.mkdir(exist_ok=True)

print("Loading data...")
# Load Pre and Post COVID data
df_pre = pd.read_csv('../Data-Nifty/nifty_bank_pre_covid.csv', index_col=False)
df_post = pd.read_csv('../Data-Nifty/nifty_bank_post_covid.csv', index_col=False)

# Drop date column if present to avoid index issues
if 'Date' in df_pre.columns:
    df_pre = df_pre.drop('Date', axis=1)
if 'Date' in df_post.columns:
    df_post = df_post.drop('Date', axis=1)

# Reset indices
df_pre = df_pre.reset_index(drop=True)
df_post = df_post.reset_index(drop=True)

# Add regime labels
df_pre['regime'] = 'Pre-COVID'
df_post['regime'] = 'Post-COVID'

# Load activation labels
activation_pre = pd.read_csv('brain_activation_pre_covid.csv')
activation_post = pd.read_csv('brain_activation_post_covid.csv')

print(f"Pre-COVID: {len(df_pre)} rows")
print(f"Post-COVID: {len(df_post)} rows")

# ==========================================
# 1. FEATURE DISTRIBUTIONS (Pre vs Post)
# ==========================================
print("\nCreating feature distribution plots...")

# Key features to visualize
key_features = [
    'rsi', 'daily_return', 'volatility_20d', 
    'price_to_ma50', 'price_to_ma200',
    'momentum_30d', 'volume_spike'
]

# Calculate Insula features if not present
if 'gap_open' not in df_pre.columns:
    df_pre['gap_open'] = ((df_pre['open'] - df_pre['close'].shift(1)) / df_pre['close'].shift(1)) * 100
    df_post['gap_open'] = ((df_post['open'] - df_post['close'].shift(1)) / df_post['close'].shift(1)) * 100

if 'intraday_range' not in df_pre.columns:
    df_pre['intraday_range'] = ((df_pre['high'] - df_pre['low']) / df_pre['open']) * 100
    df_post['intraday_range'] = ((df_post['high'] - df_post['low']) / df_post['open']) * 100

if 'volume_spike' not in df_pre.columns:
    df_pre['volume_ma_20'] = df_pre['volume'].rolling(window=20, min_periods=1).mean()
    df_post['volume_ma_20'] = df_post['volume'].rolling(window=20, min_periods=1).mean()
    df_pre['volume_spike'] = df_pre['volume'] / df_pre['volume_ma_20']
    df_post['volume_spike'] = df_post['volume'] / df_post['volume_ma_20']

# Add Insula features to visualization list
key_features.extend(['gap_open', 'intraday_range', 'volume_spike'])

# Combine data for plotting (reset index to avoid duplicates)
df_pre_subset = df_pre[key_features + ['regime']].reset_index(drop=True)
df_post_subset = df_post[key_features + ['regime']].reset_index(drop=True)
df_combined = pd.concat([df_pre_subset, df_post_subset], ignore_index=True)

# Create distribution plots
fig, axes = plt.subplots(4, 3, figsize=(18, 16))
axes = axes.flatten()

for idx, feature in enumerate(key_features):
    if idx < len(axes):
        # Get data for each regime separately
        pre_data = df_pre[feature].dropna()
        post_data = df_post[feature].dropna()
        
        # Filter outliers for better visualization using quantiles from each regime
        q1 = min(pre_data.quantile(0.01), post_data.quantile(0.01))
        q99 = max(pre_data.quantile(0.99), post_data.quantile(0.99))
        
        pre_filtered = pre_data[(pre_data >= q1) & (pre_data <= q99)]
        post_filtered = post_data[(post_data >= q1) & (post_data <= q99)]
        
        # Distribution plot
        axes[idx].hist(pre_filtered, bins=50, alpha=0.6, label='Pre-COVID', density=True, color='#3498db')
        axes[idx].hist(post_filtered, bins=50, alpha=0.6, label='Post-COVID', density=True, color='#e74c3c')
        
        axes[idx].set_xlabel(feature.replace('_', ' ').title(), fontsize=10)
        axes[idx].set_ylabel('Density', fontsize=10)
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)

# Remove extra subplots
for idx in range(len(key_features), len(axes)):
    fig.delaxes(axes[idx])

plt.suptitle('Feature Distributions: Pre-COVID vs Post-COVID', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig(output_dir / 'feature_distributions_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / 'feature_distributions_comparison.png'}")
plt.close()

# ==========================================
# 2. BOX PLOTS FOR KEY FEATURES
# ==========================================
print("\nCreating box plots...")

fig, axes = plt.subplots(4, 3, figsize=(18, 16))
axes = axes.flatten()

for idx, feature in enumerate(key_features):
    if idx < len(axes):
        # Get data for each regime separately
        pre_data = df_pre[feature].dropna()
        post_data = df_post[feature].dropna()
        
        # Filter outliers for better visualization
        q1 = min(pre_data.quantile(0.05), post_data.quantile(0.05))
        q99 = max(pre_data.quantile(0.95), post_data.quantile(0.95))
        
        pre_filtered = pre_data[(pre_data >= q1) & (pre_data <= q99)]
        post_filtered = post_data[(post_data >= q1) & (post_data <= q99)]
        
        # Prepare data for boxplot
        box_data = pd.DataFrame({
            'Value': pd.concat([pre_filtered, post_filtered]),
            'Regime': ['Pre-COVID']*len(pre_filtered) + ['Post-COVID']*len(post_filtered)
        })
        
        # Box plot
        sns.boxplot(data=box_data, x='Regime', y='Value', ax=axes[idx], palette=['#3498db', '#e74c3c'])
        axes[idx].set_xlabel('')
        axes[idx].set_ylabel(feature.replace('_', ' ').title(), fontsize=10)
        axes[idx].grid(True, alpha=0.3, axis='y')
        
        # Add mean markers
        pre_mean = pre_filtered.mean()
        post_mean = post_filtered.mean()
        axes[idx].scatter([0, 1], [pre_mean, post_mean], color='yellow', s=100, zorder=3, 
                         marker='D', edgecolors='black', label='Mean')

# Remove extra subplots
for idx in range(len(key_features), len(axes)):
    fig.delaxes(axes[idx])

plt.suptitle('Feature Box Plots: Pre-COVID vs Post-COVID', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig(output_dir / 'feature_boxplots_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / 'feature_boxplots_comparison.png'}")
plt.close()

# ==========================================
# 3. ACTIVATION FREQUENCY DISTRIBUTIONS
# ==========================================
print("\nCreating activation frequency distributions...")

brain_systems = ['value_active', 'risk_active', 'sentiment_active', 'insula_active', 'control_active']
system_names = ['Value', 'Risk', 'Sentiment', 'Insula', 'Control']

# Calculate activation frequencies per month
activation_pre['date'] = pd.to_datetime(activation_pre['date'])
activation_post['date'] = pd.to_datetime(activation_post['date'])

activation_pre['month'] = activation_pre['date'].dt.to_period('M')
activation_post['month'] = activation_post['date'].dt.to_period('M')

# Monthly activation rates
fig, axes = plt.subplots(3, 2, figsize=(16, 14))
axes = axes.flatten()

for idx, (system, name) in enumerate(zip(brain_systems, system_names)):
    if idx < len(axes):
        # Pre-COVID monthly activation
        monthly_pre = activation_pre.groupby('month')[system].mean() * 100
        monthly_post = activation_post.groupby('month')[system].mean() * 100
        
        axes[idx].hist(monthly_pre, bins=15, alpha=0.6, label='Pre-COVID', color='#3498db', density=True)
        axes[idx].hist(monthly_post, bins=15, alpha=0.6, label='Post-COVID', color='#e74c3c', density=True)
        
        axes[idx].axvline(monthly_pre.mean(), color='#3498db', linestyle='--', linewidth=2, label=f'Pre Mean: {monthly_pre.mean():.1f}%')
        axes[idx].axvline(monthly_post.mean(), color='#e74c3c', linestyle='--', linewidth=2, label=f'Post Mean: {monthly_post.mean():.1f}%')
        
        axes[idx].set_xlabel('Monthly Activation Rate (%)', fontsize=10)
        axes[idx].set_ylabel('Density', fontsize=10)
        axes[idx].set_title(f'{name} System Activation Distribution', fontsize=12, fontweight='bold')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)

# Remove extra subplot
fig.delaxes(axes[-1])

plt.suptitle('Monthly Activation Rate Distributions by Brain System', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig(output_dir / 'activation_distributions_monthly.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / 'activation_distributions_monthly.png'}")
plt.close()

# ==========================================
# 4. ACTIVATION BOX PLOTS
# ==========================================
print("\nCreating activation box plots...")

# Prepare data for box plots
activation_data = []
for system, name in zip(brain_systems, system_names):
    # Pre-COVID
    monthly_pre = activation_pre.groupby('month')[system].mean() * 100
    for rate in monthly_pre:
        activation_data.append({'System': name, 'Regime': 'Pre-COVID', 'Activation Rate (%)': rate})
    
    # Post-COVID
    monthly_post = activation_post.groupby('month')[system].mean() * 100
    for rate in monthly_post:
        activation_data.append({'System': name, 'Regime': 'Post-COVID', 'Activation Rate (%)': rate})

activation_df = pd.DataFrame(activation_data)

# Create box plot
fig, ax = plt.subplots(figsize=(14, 8))
sns.boxplot(data=activation_df, x='System', y='Activation Rate (%)', hue='Regime', 
            palette=['#3498db', '#e74c3c'], ax=ax)

# Add mean markers
for i, system in enumerate(system_names):
    pre_mean = activation_df[(activation_df['System'] == system) & 
                             (activation_df['Regime'] == 'Pre-COVID')]['Activation Rate (%)'].mean()
    post_mean = activation_df[(activation_df['System'] == system) & 
                              (activation_df['Regime'] == 'Post-COVID')]['Activation Rate (%)'].mean()
    
    ax.scatter([i - 0.2], [pre_mean], color='yellow', s=150, zorder=3, marker='D', edgecolors='black')
    ax.scatter([i + 0.2], [post_mean], color='yellow', s=150, zorder=3, marker='D', edgecolors='black')

ax.set_xlabel('Brain System', fontsize=12, fontweight='bold')
ax.set_ylabel('Monthly Activation Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Brain System Activation Rates: Pre-COVID vs Post-COVID', fontsize=14, fontweight='bold')
ax.legend(title='Regime', fontsize=10)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / 'activation_boxplots_by_system.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / 'activation_boxplots_by_system.png'}")
plt.close()

# ==========================================
# 5. FEATURE STATISTICS SUMMARY
# ==========================================
print("\nCreating feature statistics summary...")

# Calculate statistics for each feature
stats_data = []
for feature in key_features:
    pre_data = df_pre[feature].dropna()
    post_data = df_post[feature].dropna()
    
    stats_data.append({
        'Feature': feature,
        'Pre_Mean': pre_data.mean(),
        'Post_Mean': post_data.mean(),
        'Pre_Median': pre_data.median(),
        'Post_Median': post_data.median(),
        'Pre_Std': pre_data.std(),
        'Post_Std': post_data.std(),
        'Mean_Change_%': ((post_data.mean() - pre_data.mean()) / abs(pre_data.mean())) * 100
    })

stats_df = pd.DataFrame(stats_data)
stats_df.to_csv(output_dir / 'feature_statistics_comparison.csv', index=False)
print(f"✓ Saved: {output_dir / 'feature_statistics_comparison.csv'}")

# Create visualization of mean changes
fig, ax = plt.subplots(figsize=(12, 8))
colors = ['#27ae60' if x > 0 else '#e74c3c' for x in stats_df['Mean_Change_%']]
bars = ax.barh(stats_df['Feature'], stats_df['Mean_Change_%'], color=colors, alpha=0.7)

ax.axvline(0, color='black', linewidth=1)
ax.set_xlabel('Mean Change (%): Post-COVID vs Pre-COVID', fontsize=12, fontweight='bold')
ax.set_ylabel('Feature', fontsize=12, fontweight='bold')
ax.set_title('Feature Mean Changes: Pre-COVID to Post-COVID', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, stats_df['Mean_Change_%'])):
    ax.text(val + (1 if val > 0 else -1), i, f'{val:.1f}%', 
            va='center', ha='left' if val > 0 else 'right', fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / 'feature_mean_changes.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / 'feature_mean_changes.png'}")
plt.close()

# ==========================================
# 6. CORRELATION CHANGES
# ==========================================
print("\nCreating correlation comparison plots...")

# Calculate correlations
corr_pre = df_pre[key_features].corr()
corr_post = df_post[key_features].corr()
corr_diff = corr_post - corr_pre

# Plot correlation matrices
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# Pre-COVID correlations
sns.heatmap(corr_pre, annot=False, cmap='coolwarm', center=0, vmin=-1, vmax=1,
            ax=axes[0], cbar_kws={'label': 'Correlation'})
axes[0].set_title('Pre-COVID Feature Correlations', fontsize=12, fontweight='bold')

# Post-COVID correlations
sns.heatmap(corr_post, annot=False, cmap='coolwarm', center=0, vmin=-1, vmax=1,
            ax=axes[1], cbar_kws={'label': 'Correlation'})
axes[1].set_title('Post-COVID Feature Correlations', fontsize=12, fontweight='bold')

# Difference
sns.heatmap(corr_diff, annot=False, cmap='RdBu_r', center=0, vmin=-0.5, vmax=0.5,
            ax=axes[2], cbar_kws={'label': 'Correlation Change'})
axes[2].set_title('Correlation Changes (Post - Pre)', fontsize=12, fontweight='bold')

plt.suptitle('Feature Correlation Analysis', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(output_dir / 'correlation_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / 'correlation_comparison.png'}")
plt.close()

# ==========================================
# SUMMARY
# ==========================================
print("\n" + "="*60)
print("DISTRIBUTION AND BOX PLOT GENERATION COMPLETE")
print("="*60)
print("\nGenerated Files:")
print(f"  1. feature_distributions_comparison.png - Histogram distributions of all features")
print(f"  2. feature_boxplots_comparison.png - Box plots for all features")
print(f"  3. activation_distributions_monthly.png - Monthly activation rate distributions")
print(f"  4. activation_boxplots_by_system.png - Box plots of activation rates by system")
print(f"  5. feature_statistics_comparison.csv - Statistical summary of all features")
print(f"  6. feature_mean_changes.png - Bar chart of mean changes")
print(f"  7. correlation_comparison.png - Correlation matrix comparison")
print(f"\nAll plots saved in: {output_dir}")
print("\nKey Insights from Distributions:")
print(f"  - Total features analyzed: {len(key_features)}")
print(f"  - Brain systems compared: {len(system_names)}")
print(f"  - Pre-COVID samples: {len(df_pre)}")
print(f"  - Post-COVID samples: {len(df_post)}")
