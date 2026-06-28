"""
NDS (NEURO DECISION SCORE) AND STABILITY ANALYSIS
==================================================

Computes:
1. NDS: Single composite score combining Value, Risk, Sentiment systems
2. Stability metrics: Run length, entropy, regime persistence
3. Pre vs Post COVID comparison with statistical tests

NDS Formula: NDS(t) = w1·V(t) - w2·R(t) + w3·S(t)
where V, R, S are normalized continuous signals (NOT binary activations)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ks_2samp, mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("="*80)
print("NDS (NEURO DECISION SCORE) AND STABILITY ANALYSIS")
print("="*80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("\n1. LOADING DATA...")
print("-"*80)

df_pre = pd.read_csv('../../nifty_bank_pre_covid.csv')
df_post = pd.read_csv('../../nifty_bank_post_covid.csv')

df_pre['date'] = pd.to_datetime(df_pre['date'])
df_post['date'] = pd.to_datetime(df_post['date'])

print(f"Pre-COVID:  {len(df_pre)} days ({df_pre['date'].min()} to {df_pre['date'].max()})")
print(f"Post-COVID: {len(df_post)} days ({df_post['date'].min()} to {df_post['date'].max()})")

# ============================================================================
# 2. COMPUTE CONTINUOUS SIGNALS (NOT BINARY)
# ============================================================================

print("\n\n" + "="*80)
print("2. COMPUTING CONTINUOUS SIGNALS FOR NDS")
print("="*80)

def compute_signals(df):
    """Compute continuous signals for Value, Risk, Sentiment systems"""
    
    # Value signal: Daily returns (momentum indicator)
    df['daily_return'] = df['close'].pct_change()
    df['value_signal'] = df['daily_return']
    
    # Risk signal: 20-day rolling volatility (annualized)
    df['volatility_20d'] = df['daily_return'].rolling(20).std() * np.sqrt(252)
    df['risk_signal'] = df['volatility_20d']
    
    # Sentiment signal: Deviation from 50-day moving average (trend strength)
    df['ma_50'] = df['close'].rolling(50).mean()
    df['sentiment_signal'] = (df['close'] - df['ma_50']) / df['ma_50']
    
    # Remove NaN values
    df = df.dropna(subset=['value_signal', 'risk_signal', 'sentiment_signal'])
    
    return df

print("\nComputing signals for Pre-COVID period...")
df_pre = compute_signals(df_pre)
print(f"  Value signal (daily_return): range [{df_pre['value_signal'].min():.4f}, {df_pre['value_signal'].max():.4f}]")
print(f"  Risk signal (volatility):    range [{df_pre['risk_signal'].min():.4f}, {df_pre['risk_signal'].max():.4f}]")
print(f"  Sentiment signal (MA dev):   range [{df_pre['sentiment_signal'].min():.4f}, {df_pre['sentiment_signal'].max():.4f}]")

print("\nComputing signals for Post-COVID period...")
df_post = compute_signals(df_post)
print(f"  Value signal (daily_return): range [{df_post['value_signal'].min():.4f}, {df_post['value_signal'].max():.4f}]")
print(f"  Risk signal (volatility):    range [{df_post['risk_signal'].min():.4f}, {df_post['risk_signal'].max():.4f}]")
print(f"  Sentiment signal (MA dev):   range [{df_post['sentiment_signal'].min():.4f}, {df_post['sentiment_signal'].max():.4f}]")

# ============================================================================
# 3. NORMALIZE SIGNALS (Z-SCORE USING PRE-COVID STATS)
# ============================================================================

print("\n\n" + "="*80)
print("3. NORMALIZING SIGNALS (Z-SCORE)")
print("="*80)

# Compute normalization parameters from Pre-COVID data ONLY
value_mean = df_pre['value_signal'].mean()
value_std = df_pre['value_signal'].std()

risk_mean = df_pre['risk_signal'].mean()
risk_std = df_pre['risk_signal'].std()

sentiment_mean = df_pre['sentiment_signal'].mean()
sentiment_std = df_pre['sentiment_signal'].std()

print("\nNormalization parameters (from Pre-COVID training data):")
print(f"  Value:     μ={value_mean:.6f}, σ={value_std:.6f}")
print(f"  Risk:      μ={risk_mean:.6f}, σ={risk_std:.6f}")
print(f"  Sentiment: μ={sentiment_mean:.6f}, σ={sentiment_std:.6f}")

# Apply normalization to both periods
df_pre['V_norm'] = (df_pre['value_signal'] - value_mean) / value_std
df_pre['R_norm'] = (df_pre['risk_signal'] - risk_mean) / risk_std
df_pre['S_norm'] = (df_pre['sentiment_signal'] - sentiment_mean) / sentiment_std

df_post['V_norm'] = (df_post['value_signal'] - value_mean) / value_std
df_post['R_norm'] = (df_post['risk_signal'] - risk_mean) / risk_std
df_post['S_norm'] = (df_post['sentiment_signal'] - sentiment_mean) / sentiment_std

print("\n✓ Normalized signals computed")
print(f"  Pre-COVID V_norm:  mean={df_pre['V_norm'].mean():.4f}, std={df_pre['V_norm'].std():.4f}")
print(f"  Post-COVID V_norm: mean={df_post['V_norm'].mean():.4f}, std={df_post['V_norm'].std():.4f}")

# ============================================================================
# 4. COMPUTE NDS (NEURO DECISION SCORE)
# ============================================================================

print("\n\n" + "="*80)
print("4. COMPUTING NDS (NEURO DECISION SCORE)")
print("="*80)

# Weights (start with equal weights as recommended)
w1 = 1.0  # Value
w2 = 1.0  # Risk
w3 = 1.0  # Sentiment

print(f"\nWeights: w1={w1}, w2={w2}, w3={w3}")
print("Formula: NDS(t) = w1·V(t) - w2·R(t) + w3·S(t)")
print("         (positive NDS = rational/trend-driven, negative = fear-dominant)")

# Compute NDS
df_pre['NDS'] = w1 * df_pre['V_norm'] - w2 * df_pre['R_norm'] + w3 * df_pre['S_norm']
df_post['NDS'] = w1 * df_post['V_norm'] - w2 * df_post['R_norm'] + w3 * df_post['S_norm']

# NDS statistics
pre_nds_mean = df_pre['NDS'].mean()
pre_nds_std = df_pre['NDS'].std()
pre_nds_median = df_pre['NDS'].median()

post_nds_mean = df_post['NDS'].mean()
post_nds_std = df_post['NDS'].std()
post_nds_median = df_post['NDS'].median()

print("\n" + "-"*80)
print("NDS SUMMARY STATISTICS")
print("-"*80)
print(f"                  Pre-COVID    Post-COVID   Change")
print(f"Mean:             {pre_nds_mean:+.4f}       {post_nds_mean:+.4f}       {(post_nds_mean - pre_nds_mean):+.4f}")
print(f"Std Dev:          {pre_nds_std:.4f}        {post_nds_std:.4f}        {(post_nds_std - pre_nds_std):+.4f}")
print(f"Median:           {pre_nds_median:+.4f}       {post_nds_median:+.4f}       {(post_nds_median - pre_nds_median):+.4f}")

print(f"\nInterpretation:")
print(f"  Pre-COVID:  Mean NDS = {pre_nds_mean:+.4f} ({'Rational-dominant' if pre_nds_mean > 0 else 'Fear-dominant'})")
print(f"  Post-COVID: Mean NDS = {post_nds_mean:+.4f} ({'Rational-dominant' if post_nds_mean > 0 else 'Fear-dominant'})")
print(f"  Change:     {(post_nds_mean - pre_nds_mean):+.4f} ({'More rational' if post_nds_mean > pre_nds_mean else 'More fearful'})")

# Statistical tests
ks_stat, ks_p = ks_2samp(df_pre['NDS'], df_post['NDS'])
mw_stat, mw_p = mannwhitneyu(df_pre['NDS'], df_post['NDS'], alternative='two-sided')

print("\n" + "-"*80)
print("STATISTICAL TESTS: NDS Distribution Comparison")
print("-"*80)
print(f"Kolmogorov-Smirnov Test:")
print(f"  Statistic: {ks_stat:.4f}")
print(f"  P-value:   {ks_p:.6f}")
print(f"  Result:    {'Distributions are DIFFERENT (p<0.05)' if ks_p < 0.05 else 'Cannot reject equal distributions'}")

print(f"\nMann-Whitney U Test:")
print(f"  Statistic: {mw_stat:.2f}")
print(f"  P-value:   {mw_p:.6f}")
print(f"  Result:    {'Medians are DIFFERENT (p<0.05)' if mw_p < 0.05 else 'Cannot reject equal medians'}")

# ============================================================================
# 5. STABILITY ANALYSIS - RUN LENGTH
# ============================================================================

print("\n\n" + "="*80)
print("5. STABILITY ANALYSIS: RUN LENGTH")
print("="*80)

# Load activation data (binary)
print("\nLoading binary activation data...")
df_pre_act = pd.read_csv('Results_PrePost_Comparison/pre_covid_activations.csv')
df_post_act = pd.read_csv('Results_PrePost_Comparison/post_covid_activations.csv')

print(f"  Pre-COVID activations:  {len(df_pre_act)} rows")
print(f"  Post-COVID activations: {len(df_post_act)} rows")

def compute_run_lengths(series):
    """Compute run lengths (consecutive 1's) for a binary series"""
    runs = []
    current_run = 0
    
    for val in series:
        if val == 1:
            current_run += 1
        else:
            if current_run > 0:
                runs.append(current_run)
            current_run = 0
    
    if current_run > 0:  # Add final run if series ends with 1
        runs.append(current_run)
    
    return runs if len(runs) > 0 else [0]

systems = ['value_active', 'risk_active', 'sentiment_active', 'insula_active', 'control_active']

print("\n" + "-"*80)
print("AVERAGE RUN LENGTH (Consecutive Days System Stays Active)")
print("-"*80)
print(f"System        Pre-COVID    Post-COVID   Change       Interpretation")

run_results = []

for system in systems:
    pre_runs = compute_run_lengths(df_pre_act[system])
    post_runs = compute_run_lengths(df_post_act[system])
    
    pre_avg = np.mean(pre_runs)
    post_avg = np.mean(post_runs)
    change = post_avg - pre_avg
    pct_change = (change / pre_avg) * 100 if pre_avg > 0 else 0
    
    interpretation = "More stable" if change > 0 else "Less stable"
    
    print(f"{system:15s} {pre_avg:7.2f}      {post_avg:7.2f}      {change:+6.2f}       {interpretation}")
    
    run_results.append({
        'System': system.replace('_active', '').capitalize(),
        'Pre_Avg_Run': pre_avg,
        'Post_Avg_Run': post_avg,
        'Change': change,
        'Pct_Change': pct_change
    })

print("\nInterpretation:")
print("  - Higher run length = More stable (system persists longer)")
print("  - Lower run length = Less stable (frequent switching)")

# ============================================================================
# 6. STABILITY ANALYSIS - ENTROPY
# ============================================================================

print("\n\n" + "="*80)
print("6. STABILITY ANALYSIS: ACTIVATION ENTROPY")
print("="*80)

def compute_entropy(activations_df):
    """Compute Shannon entropy of activation distribution"""
    # For each system, compute proportion active
    proportions = []
    for system in systems:
        p_active = activations_df[system].mean()
        proportions.append(p_active)
    
    # Shannon entropy: H = -Σ p_i log(p_i)
    # We have 5 systems, each with proportion p_i
    entropy = 0
    for p in proportions:
        if p > 0 and p < 1:  # Avoid log(0)
            entropy += -p * np.log2(p) - (1-p) * np.log2(1-p)
    
    return entropy

pre_entropy = compute_entropy(df_pre_act)
post_entropy = compute_entropy(df_post_act)

print(f"\nShannon Entropy (sum across all systems):")
print(f"  Pre-COVID:  {pre_entropy:.4f} bits")
print(f"  Post-COVID: {post_entropy:.4f} bits")
print(f"  Change:     {(post_entropy - pre_entropy):+.4f} bits")

print(f"\nInterpretation:")
if post_entropy > pre_entropy:
    print(f"  ↑ Higher entropy Post-COVID = More uncertain/unstable activation patterns")
else:
    print(f"  ↓ Lower entropy Post-COVID = More predictable activation patterns")

# ============================================================================
# 7. NDS REGIME CLASSIFICATION
# ============================================================================

print("\n\n" + "="*80)
print("7. NDS REGIME CLASSIFICATION")
print("="*80)

# Define NDS regimes based on thresholds
def classify_nds_regime(nds_value):
    """Classify NDS into cognitive regimes"""
    if nds_value > 0.5:
        return 'Rational'
    elif nds_value < -0.5:
        return 'Fear-Dominant'
    else:
        return 'Mixed/Conflicted'

df_pre['NDS_regime'] = df_pre['NDS'].apply(classify_nds_regime)
df_post['NDS_regime'] = df_post['NDS'].apply(classify_nds_regime)

# Count regime frequencies
pre_regimes = df_pre['NDS_regime'].value_counts(normalize=True) * 100
post_regimes = df_post['NDS_regime'].value_counts(normalize=True) * 100

print("\nNDS Regime Frequency (% of days):")
print("-"*80)
print(f"Regime              Pre-COVID    Post-COVID   Change")
for regime in ['Rational', 'Mixed/Conflicted', 'Fear-Dominant']:
    pre_pct = pre_regimes.get(regime, 0)
    post_pct = post_regimes.get(regime, 0)
    change = post_pct - pre_pct
    print(f"{regime:20s} {pre_pct:6.2f}%      {post_pct:6.2f}%      {change:+6.2f}%")

# Compute regime persistence (run length for NDS regimes)
def regime_run_lengths(regime_series):
    """Compute average run length for each regime type"""
    runs = {'Rational': [], 'Mixed/Conflicted': [], 'Fear-Dominant': []}
    current_regime = None
    current_run = 0
    
    for regime in regime_series:
        if regime == current_regime:
            current_run += 1
        else:
            if current_regime is not None and current_run > 0:
                runs[current_regime].append(current_run)
            current_regime = regime
            current_run = 1
    
    if current_regime is not None and current_run > 0:
        runs[current_regime].append(current_run)
    
    return {k: np.mean(v) if len(v) > 0 else 0 for k, v in runs.items()}

pre_regime_runs = regime_run_lengths(df_pre['NDS_regime'])
post_regime_runs = regime_run_lengths(df_post['NDS_regime'])

print("\n" + "-"*80)
print("NDS Regime Persistence (Average Consecutive Days)")
print("-"*80)
print(f"Regime              Pre-COVID    Post-COVID   Change")
for regime in ['Rational', 'Mixed/Conflicted', 'Fear-Dominant']:
    pre_run = pre_regime_runs.get(regime, 0)
    post_run = post_regime_runs.get(regime, 0)
    change = post_run - pre_run
    print(f"{regime:20s} {pre_run:6.2f}       {post_run:6.2f}       {change:+6.2f} days")

# ============================================================================
# 8. SAVE RESULTS
# ============================================================================

print("\n\n" + "="*80)
print("8. SAVING RESULTS")
print("="*80)

import os
os.makedirs('Results_NDS_Stability', exist_ok=True)

# NDS time series
nds_ts = pd.DataFrame({
    'Period': ['Pre-COVID'] * len(df_pre) + ['Post-COVID'] * len(df_post),
    'Date': pd.concat([df_pre['date'], df_post['date']]).reset_index(drop=True),
    'NDS': pd.concat([df_pre['NDS'], df_post['NDS']]).reset_index(drop=True),
    'NDS_regime': pd.concat([df_pre['NDS_regime'], df_post['NDS_regime']]).reset_index(drop=True),
    'V_norm': pd.concat([df_pre['V_norm'], df_post['V_norm']]).reset_index(drop=True),
    'R_norm': pd.concat([df_pre['R_norm'], df_post['R_norm']]).reset_index(drop=True),
    'S_norm': pd.concat([df_pre['S_norm'], df_post['S_norm']]).reset_index(drop=True)
})
nds_ts.to_csv('Results_NDS_Stability/nds_timeseries.csv', index=False)
print("✓ Saved: Results_NDS_Stability/nds_timeseries.csv")

# Summary statistics
summary_data = {
    'Metric': [
        'NDS Mean',
        'NDS Std Dev',
        'NDS Median',
        'Rational Regime (%)',
        'Fear-Dominant Regime (%)',
        'Mixed Regime (%)',
        'Activation Entropy (bits)',
        'Value Run Length (days)',
        'Risk Run Length (days)',
        'Sentiment Run Length (days)',
        'Insula Run Length (days)',
        'Control Run Length (days)'
    ],
    'Pre_COVID': [
        f"{pre_nds_mean:.4f}",
        f"{pre_nds_std:.4f}",
        f"{pre_nds_median:.4f}",
        f"{pre_regimes.get('Rational', 0):.2f}",
        f"{pre_regimes.get('Fear-Dominant', 0):.2f}",
        f"{pre_regimes.get('Mixed/Conflicted', 0):.2f}",
        f"{pre_entropy:.4f}",
        f"{run_results[0]['Pre_Avg_Run']:.2f}",
        f"{run_results[1]['Pre_Avg_Run']:.2f}",
        f"{run_results[2]['Pre_Avg_Run']:.2f}",
        f"{run_results[3]['Pre_Avg_Run']:.2f}",
        f"{run_results[4]['Pre_Avg_Run']:.2f}"
    ],
    'Post_COVID': [
        f"{post_nds_mean:.4f}",
        f"{post_nds_std:.4f}",
        f"{post_nds_median:.4f}",
        f"{post_regimes.get('Rational', 0):.2f}",
        f"{post_regimes.get('Fear-Dominant', 0):.2f}",
        f"{post_regimes.get('Mixed/Conflicted', 0):.2f}",
        f"{post_entropy:.4f}",
        f"{run_results[0]['Post_Avg_Run']:.2f}",
        f"{run_results[1]['Post_Avg_Run']:.2f}",
        f"{run_results[2]['Post_Avg_Run']:.2f}",
        f"{run_results[3]['Post_Avg_Run']:.2f}",
        f"{run_results[4]['Post_Avg_Run']:.2f}"
    ],
    'Change': [
        f"{(post_nds_mean - pre_nds_mean):+.4f}",
        f"{(post_nds_std - pre_nds_std):+.4f}",
        f"{(post_nds_median - pre_nds_median):+.4f}",
        f"{(post_regimes.get('Rational', 0) - pre_regimes.get('Rational', 0)):+.2f}",
        f"{(post_regimes.get('Fear-Dominant', 0) - pre_regimes.get('Fear-Dominant', 0)):+.2f}",
        f"{(post_regimes.get('Mixed/Conflicted', 0) - pre_regimes.get('Mixed/Conflicted', 0)):+.2f}",
        f"{(post_entropy - pre_entropy):+.4f}",
        f"{run_results[0]['Change']:+.2f}",
        f"{run_results[1]['Change']:+.2f}",
        f"{run_results[2]['Change']:+.2f}",
        f"{run_results[3]['Change']:+.2f}",
        f"{run_results[4]['Change']:+.2f}"
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('Results_NDS_Stability/nds_stability_summary.csv', index=False)
print("✓ Saved: Results_NDS_Stability/nds_stability_summary.csv")

# Statistical tests
tests_df = pd.DataFrame({
    'Test': ['K-S Test (NDS Distribution)', 'Mann-Whitney U (NDS Median)'],
    'Statistic': [f"{ks_stat:.4f}", f"{mw_stat:.2f}"],
    'P_Value': [f"{ks_p:.6f}", f"{mw_p:.6f}"],
    'Result': [
        'Significant (p<0.05)' if ks_p < 0.05 else 'Not significant',
        'Significant (p<0.05)' if mw_p < 0.05 else 'Not significant'
    ]
})
tests_df.to_csv('Results_NDS_Stability/statistical_tests.csv', index=False)
print("✓ Saved: Results_NDS_Stability/statistical_tests.csv")

# ============================================================================
# 9. VISUALIZATIONS
# ============================================================================

print("\n\n" + "="*80)
print("9. GENERATING VISUALIZATIONS")
print("="*80)

# Plot 1: NDS Time Series
fig, axes = plt.subplots(2, 1, figsize=(16, 10))

axes[0].plot(df_pre['date'], df_pre['NDS'], color='#3498db', linewidth=1, alpha=0.7, label='Daily NDS')
axes[0].axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.3)
axes[0].axhline(y=pre_nds_mean, color='#3498db', linestyle='--', linewidth=2, label=f'Mean: {pre_nds_mean:.3f}')
axes[0].fill_between(df_pre['date'], 0, df_pre['NDS'], where=(df_pre['NDS'] > 0), color='green', alpha=0.2, label='Rational')
axes[0].fill_between(df_pre['date'], 0, df_pre['NDS'], where=(df_pre['NDS'] < 0), color='red', alpha=0.2, label='Fear')
axes[0].set_ylabel('NDS', fontweight='bold', fontsize=12)
axes[0].set_title('Pre-COVID: Neuro Decision Score (NDS) Over Time', fontweight='bold', fontsize=13)
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)

axes[1].plot(df_post['date'], df_post['NDS'], color='#e74c3c', linewidth=1, alpha=0.7, label='Daily NDS')
axes[1].axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.3)
axes[1].axhline(y=post_nds_mean, color='#e74c3c', linestyle='--', linewidth=2, label=f'Mean: {post_nds_mean:.3f}')
axes[1].fill_between(df_post['date'], 0, df_post['NDS'], where=(df_post['NDS'] > 0), color='green', alpha=0.2, label='Rational')
axes[1].fill_between(df_post['date'], 0, df_post['NDS'], where=(df_post['NDS'] < 0), color='red', alpha=0.2, label='Fear')
axes[1].set_xlabel('Date', fontweight='bold', fontsize=12)
axes[1].set_ylabel('NDS', fontweight='bold', fontsize=12)
axes[1].set_title('Post-COVID: Neuro Decision Score (NDS) Over Time', fontweight='bold', fontsize=13)
axes[1].legend(loc='upper right')
axes[1].grid(True, alpha=0.3)

plt.suptitle('Neuro Decision Score: Pre vs Post COVID', fontsize=15, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('Results_NDS_Stability/nds_timeseries.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Results_NDS_Stability/nds_timeseries.png")
plt.close()

# Plot 2: NDS Distribution Comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].hist(df_pre['NDS'], bins=40, color='#3498db', alpha=0.7, edgecolor='black', density=True)
axes[0].axvline(x=pre_nds_mean, color='red', linestyle='--', linewidth=2.5, label=f'Mean: {pre_nds_mean:.3f}')
axes[0].axvline(x=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5, label='Neutral')
axes[0].set_xlabel('NDS Value', fontweight='bold', fontsize=12)
axes[0].set_ylabel('Density', fontweight='bold', fontsize=12)
axes[0].set_title(f'Pre-COVID NDS Distribution\nMean={pre_nds_mean:.3f}, σ={pre_nds_std:.3f}', fontweight='bold', fontsize=13)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].hist(df_post['NDS'], bins=40, color='#e74c3c', alpha=0.7, edgecolor='black', density=True)
axes[1].axvline(x=post_nds_mean, color='red', linestyle='--', linewidth=2.5, label=f'Mean: {post_nds_mean:.3f}')
axes[1].axvline(x=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5, label='Neutral')
axes[1].set_xlabel('NDS Value', fontweight='bold', fontsize=12)
axes[1].set_ylabel('Density', fontweight='bold', fontsize=12)
axes[1].set_title(f'Post-COVID NDS Distribution\nMean={post_nds_mean:.3f}, σ={post_nds_std:.3f}', fontweight='bold', fontsize=13)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle(f'NDS Distribution Comparison (K-S test p={ks_p:.4f})', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('Results_NDS_Stability/nds_distributions.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Results_NDS_Stability/nds_distributions.png")
plt.close()

# Plot 3: NDS Regime Frequencies
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

regimes = ['Rational', 'Mixed/Conflicted', 'Fear-Dominant']
pre_vals = [pre_regimes.get(r, 0) for r in regimes]
post_vals = [post_regimes.get(r, 0) for r in regimes]

x = np.arange(len(regimes))
width = 0.35

bars1 = ax.bar(x - width/2, pre_vals, width, label='Pre-COVID', color='#3498db', edgecolor='black')
bars2 = ax.bar(x + width/2, post_vals, width, label='Post-COVID', color='#e74c3c', edgecolor='black')

ax.set_xlabel('NDS Regime', fontweight='bold', fontsize=12)
ax.set_ylabel('Frequency (%)', fontweight='bold', fontsize=12)
ax.set_title('NDS Regime Distribution: Pre vs Post COVID', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(regimes)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('Results_NDS_Stability/nds_regimes.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Results_NDS_Stability/nds_regimes.png")
plt.close()

# Plot 4: System Run Lengths Comparison
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

system_names = ['Value', 'Risk', 'Sentiment', 'Insula', 'Control']
pre_runs = [r['Pre_Avg_Run'] for r in run_results]
post_runs = [r['Post_Avg_Run'] for r in run_results]

x = np.arange(len(system_names))
width = 0.35

bars1 = ax.bar(x - width/2, pre_runs, width, label='Pre-COVID', color='#3498db', edgecolor='black')
bars2 = ax.bar(x + width/2, post_runs, width, label='Post-COVID', color='#e74c3c', edgecolor='black')

ax.set_xlabel('Brain System', fontweight='bold', fontsize=12)
ax.set_ylabel('Average Run Length (days)', fontweight='bold', fontsize=12)
ax.set_title('System Stability: Average Consecutive Activation Days', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(system_names)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('Results_NDS_Stability/run_length_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Results_NDS_Stability/run_length_comparison.png")
plt.close()

print("\n" + "="*80)
print("NDS AND STABILITY ANALYSIS COMPLETE")
print("="*80)
print(f"\n📊 KEY FINDINGS:")
print(f"  • NDS shifted from {pre_nds_mean:+.3f} to {post_nds_mean:+.3f} (p={ks_p:.4f})")
print(f"  • {'Fear-dominant' if post_nds_mean < pre_nds_mean else 'Rational'} regime {'increased' if post_nds_mean < pre_nds_mean else 'decreased'} Post-COVID")
print(f"  • Activation entropy: {pre_entropy:.3f} → {post_entropy:.3f} bits ({'more unstable' if post_entropy > pre_entropy else 'more stable'})")
print(f"  • All results saved to Results_NDS_Stability/")
print("="*80)
