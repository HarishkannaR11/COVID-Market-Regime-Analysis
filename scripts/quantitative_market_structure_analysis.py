"""
QUANTITATIVE MARKET STRUCTURE ANALYSIS: NIFTY BANK INDEX
=========================================================

Empirical identification of structural changes in market behavior
Pre-COVID vs Post-COVID periods using econometric methods.

Focus: Volatility, regime stability, return distribution, liquidity dynamics,
       and technical indicator sensitivity at index level.

NO predictions, NO trading advice, NO individual bank attribution.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import jarque_bera, shapiro, kstest, anderson
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# ============================================================================
# 1. DATA LOADING AND PREPARATION
# ============================================================================

print("="*80)
print("QUANTITATIVE MARKET STRUCTURE ANALYSIS: NIFTY BANK INDEX")
print("="*80)
print("\n1. LOADING DATA...")
print("-"*80)

# Load data
df_pre = pd.read_csv('../../nifty_bank_pre_covid.csv')
df_post = pd.read_csv('../../nifty_bank_post_covid.csv')

# Convert dates
df_pre['date'] = pd.to_datetime(df_pre['date'])
df_post['date'] = pd.to_datetime(df_post['date'])

print(f"Pre-COVID Period: {df_pre['date'].min()} to {df_pre['date'].max()}")
print(f"  - Trading days: {len(df_pre)}")
print(f"  - Duration: {(df_pre['date'].max() - df_pre['date'].min()).days} calendar days")

print(f"\nPost-COVID Period: {df_post['date'].min()} to {df_post['date'].max()}")
print(f"  - Trading days: {len(df_post)}")
print(f"  - Duration: {(df_post['date'].max() - df_post['date'].min()).days} calendar days")

# Calculate returns
df_pre['daily_return'] = df_pre['close'].pct_change()
df_post['daily_return'] = df_post['close'].pct_change()

# Remove first NaN
df_pre = df_pre.dropna(subset=['daily_return'])
df_post = df_post.dropna(subset=['daily_return'])

# ============================================================================
# 2. VOLATILITY STRUCTURE ANALYSIS
# ============================================================================

print("\n\n" + "="*80)
print("2. VOLATILITY STRUCTURE ANALYSIS")
print("="*80)

# Calculate realized volatility measures
df_pre['abs_return'] = df_pre['daily_return'].abs()
df_post['abs_return'] = df_post['daily_return'].abs()

df_pre['squared_return'] = df_pre['daily_return'] ** 2
df_post['squared_return'] = df_post['daily_return'] ** 2

# Rolling volatility (20-day window)
df_pre['vol_20d'] = df_pre['daily_return'].rolling(20).std() * np.sqrt(252)
df_post['vol_20d'] = df_post['daily_return'].rolling(20).std() * np.sqrt(252)

# Volatility metrics
pre_vol = df_pre['daily_return'].std() * np.sqrt(252)
post_vol = df_post['daily_return'].std() * np.sqrt(252)

pre_mean_vol = df_pre['vol_20d'].mean()
post_mean_vol = df_post['vol_20d'].mean()

# Downside volatility (semi-deviation)
pre_downside = df_pre[df_pre['daily_return'] < 0]['daily_return'].std() * np.sqrt(252)
post_downside = df_post[df_post['daily_return'] < 0]['daily_return'].std() * np.sqrt(252)

# Volatility clustering: Autocorrelation of squared returns
from statsmodels.tsa.stattools import acf

pre_acf = acf(df_pre['squared_return'].dropna(), nlags=20, fft=True)[1]
post_acf = acf(df_post['squared_return'].dropna(), nlags=20, fft=True)[1]

pre_clustering = pre_acf  # Average of first 20 lags
post_clustering = post_acf

print("\nA. Realized Volatility (Annualized)")
print("-"*80)
print(f"Pre-COVID:  {pre_vol:.2%}")
print(f"Post-COVID: {post_vol:.2%}")
print(f"Change:     {(post_vol - pre_vol)/pre_vol:+.1%} ({post_vol/pre_vol:.2f}x multiplier)")

print("\nB. Downside Volatility (Negative Returns Only)")
print("-"*80)
print(f"Pre-COVID:  {pre_downside:.2%}")
print(f"Post-COVID: {post_downside:.2%}")
print(f"Change:     {(post_downside - pre_downside)/pre_downside:+.1%}")

print("\nC. Volatility Clustering (Autocorrelation of Squared Returns, Lag 1)")
print("-"*80)
print(f"Pre-COVID:  {pre_acf:.4f}")
print(f"Post-COVID: {post_acf:.4f}")
print(f"Change:     {(post_acf - pre_acf):+.4f}")
print("\nInterpretation: Higher autocorrelation indicates stronger volatility clustering")
print("(today's volatility predicts tomorrow's volatility)")

# Levene's test for variance equality
from scipy.stats import levene
levene_stat, levene_p = levene(df_pre['daily_return'].dropna(), 
                                 df_post['daily_return'].dropna())

print("\nD. Statistical Test: Variance Equality (Levene's Test)")
print("-"*80)
print(f"Test Statistic: {levene_stat:.4f}")
print(f"P-value:        {levene_p:.6f}")
print(f"Conclusion:     {'Variances are DIFFERENT (reject H0)' if levene_p < 0.05 else 'Cannot reject equal variance'}")

# ============================================================================
# 3. RETURN DISTRIBUTION COMPARISON
# ============================================================================

print("\n\n" + "="*80)
print("3. RETURN DISTRIBUTION ANALYSIS")
print("="*80)

# Distribution moments
pre_mean = df_pre['daily_return'].mean()
post_mean = df_post['daily_return'].mean()

pre_skew = df_pre['daily_return'].skew()
post_skew = df_post['daily_return'].skew()

pre_kurt = df_pre['daily_return'].kurtosis()
post_kurt = df_post['daily_return'].kurtosis()

# Tail risk: 5th and 95th percentiles
pre_var_5 = df_pre['daily_return'].quantile(0.05)
post_var_5 = df_post['daily_return'].quantile(0.05)

pre_var_95 = df_pre['daily_return'].quantile(0.95)
post_var_95 = df_post['daily_return'].quantile(0.95)

print("\nA. Central Moments")
print("-"*80)
print(f"                 Pre-COVID    Post-COVID   Change")
print(f"Mean (daily):    {pre_mean:.4%}     {post_mean:.4%}      {(post_mean - pre_mean):.4%}")
print(f"Std Dev:         {df_pre['daily_return'].std():.4%}     {df_post['daily_return'].std():.4%}      {(df_post['daily_return'].std() - df_pre['daily_return'].std()):.4%}")
print(f"Skewness:        {pre_skew:+.4f}      {post_skew:+.4f}       {(post_skew - pre_skew):+.4f}")
print(f"Kurtosis:        {pre_kurt:+.4f}      {post_kurt:+.4f}       {(post_kurt - pre_kurt):+.4f}")

print("\nInterpretation:")
print(f"  - Skewness: Pre={pre_skew:.2f} {'(left tail)' if pre_skew < 0 else '(right tail)'}, "
      f"Post={post_skew:.2f} {'(left tail)' if post_skew < 0 else '(right tail)'}")
print(f"  - Kurtosis: Pre={pre_kurt:.2f} {'(fat tails)' if pre_kurt > 0 else '(thin tails)'}, "
      f"Post={post_kurt:.2f} {'(fat tails)' if post_kurt > 0 else '(thin tails)'}")

print("\nB. Tail Risk (5th and 95th Percentiles)")
print("-"*80)
print(f"5th Percentile:  Pre={pre_var_5:.3%}, Post={post_var_5:.3%} (worse tail: {'Post' if post_var_5 < pre_var_5 else 'Pre'})")
print(f"95th Percentile: Pre={pre_var_95:.3%}, Post={post_var_95:.3%}")

# Normality tests
jb_pre_stat, jb_pre_p = jarque_bera(df_pre['daily_return'].dropna())
jb_post_stat, jb_post_p = jarque_bera(df_post['daily_return'].dropna())

print("\nC. Normality Tests (Jarque-Bera)")
print("-"*80)
print(f"Pre-COVID:  Statistic={jb_pre_stat:.4f}, p-value={jb_pre_p:.6f}")
print(f"            {'REJECT normality' if jb_pre_p < 0.05 else 'Cannot reject normality'}")
print(f"Post-COVID: Statistic={jb_post_stat:.4f}, p-value={jb_post_p:.6f}")
print(f"            {'REJECT normality' if jb_post_p < 0.05 else 'Cannot reject normality'}")

# Kolmogorov-Smirnov test for distribution equality
ks_stat, ks_p = stats.ks_2samp(df_pre['daily_return'].dropna(), 
                                df_post['daily_return'].dropna())

print("\nD. Distribution Equality Test (Kolmogorov-Smirnov)")
print("-"*80)
print(f"Test Statistic: {ks_stat:.4f}")
print(f"P-value:        {ks_p:.6f}")
print(f"Conclusion:     {'Distributions are DIFFERENT (reject H0)' if ks_p < 0.05 else 'Cannot reject equal distributions'}")

# ============================================================================
# 4. LIQUIDITY AND VOLUME DYNAMICS
# ============================================================================

print("\n\n" + "="*80)
print("4. LIQUIDITY AND VOLUME DYNAMICS")
print("="*80)

# Volume statistics
pre_vol_mean = df_pre['volume'].mean()
post_vol_mean = df_post['volume'].mean()

pre_vol_std = df_pre['volume'].std()
post_vol_std = df_post['volume'].std()

# Volume-volatility correlation
pre_vol_corr = df_pre['volume'].corr(df_pre['abs_return'])
post_vol_corr = df_post['volume'].corr(df_post['abs_return'])

# Volume spikes (>2 std above mean)
df_pre['vol_spike'] = df_pre['volume'] > (pre_vol_mean + 2*pre_vol_std)
df_post['vol_spike'] = df_post['volume'] > (post_vol_mean + 2*post_vol_std)

pre_spike_freq = df_pre['vol_spike'].mean()
post_spike_freq = df_post['vol_spike'].mean()

print("\nA. Volume Statistics")
print("-"*80)
print(f"Mean Volume:     Pre={pre_vol_mean:,.0f}, Post={post_vol_mean:,.0f} ({(post_vol_mean/pre_vol_mean - 1):+.1%})")
print(f"Volume Std Dev:  Pre={pre_vol_std:,.0f}, Post={post_vol_std:,.0f} ({(post_vol_std/pre_vol_std - 1):+.1%})")

print("\nB. Volume-Volatility Relationship")
print("-"*80)
print(f"Correlation (Volume vs Absolute Return):")
print(f"  Pre-COVID:  {pre_vol_corr:.4f}")
print(f"  Post-COVID: {post_vol_corr:.4f}")
print(f"  Change:     {(post_vol_corr - pre_vol_corr):+.4f}")
print("\nInterpretation: Higher correlation = volume increases with volatility")

print("\nC. Volume Spike Frequency (>2σ above mean)")
print("-"*80)
print(f"Pre-COVID:  {pre_spike_freq:.2%} of days")
print(f"Post-COVID: {post_spike_freq:.2%} of days")
print(f"Change:     {(post_spike_freq - pre_spike_freq):+.2%} percentage points")

# ============================================================================
# 5. TECHNICAL INDICATOR SENSITIVITY
# ============================================================================

print("\n\n" + "="*80)
print("5. TECHNICAL INDICATOR SENSITIVITY ANALYSIS")
print("="*80)

# RSI
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df_pre['rsi'] = calculate_rsi(df_pre['close'])
df_post['rsi'] = calculate_rsi(df_post['close'])

# RSI extreme signals
pre_rsi_ob = (df_pre['rsi'] > 70).mean()
post_rsi_ob = (df_post['rsi'] > 70).mean()

pre_rsi_os = (df_pre['rsi'] < 30).mean()
post_rsi_os = (df_post['rsi'] < 30).mean()

# Moving averages
df_pre['ma_50'] = df_pre['close'].rolling(50).mean()
df_post['ma_50'] = df_post['close'].rolling(50).mean()

df_pre['ma_200'] = df_pre['close'].rolling(200).mean()
df_post['ma_200'] = df_post['close'].rolling(200).mean()

# Price-MA deviation
df_pre['dev_ma50'] = ((df_pre['close'] - df_pre['ma_50']) / df_pre['ma_50']).abs()
df_post['dev_ma50'] = ((df_post['close'] - df_post['ma_50']) / df_post['ma_50']).abs()

pre_dev_mean = df_pre['dev_ma50'].mean()
post_dev_mean = df_post['dev_ma50'].mean()

# Crossover frequency
df_pre['above_ma50'] = df_pre['close'] > df_pre['ma_50']
df_post['above_ma50'] = df_post['close'] > df_post['ma_50']

pre_crossovers = df_pre['above_ma50'].diff().abs().sum()
post_crossovers = df_post['above_ma50'].diff().abs().sum()

print("\nA. RSI Extreme Signal Frequency")
print("-"*80)
print(f"Overbought (RSI > 70):")
print(f"  Pre-COVID:  {pre_rsi_ob:.2%} of days")
print(f"  Post-COVID: {post_rsi_ob:.2%} of days")
print(f"  Change:     {(post_rsi_ob - pre_rsi_ob):+.2%} pp")

print(f"\nOversold (RSI < 30):")
print(f"  Pre-COVID:  {pre_rsi_os:.2%} of days")
print(f"  Post-COVID: {post_rsi_os:.2%} of days")
print(f"  Change:     {(post_rsi_os - pre_rsi_os):+.2%} pp")

print("\nB. Moving Average Deviation")
print("-"*80)
print(f"Mean Absolute Deviation from 50-day MA:")
print(f"  Pre-COVID:  {pre_dev_mean:.3%}")
print(f"  Post-COVID: {post_dev_mean:.3%}")
print(f"  Change:     {(post_dev_mean - pre_dev_mean):+.3%} pp")
print("\nInterpretation: Larger deviation = more volatile price swings around trend")

print("\nC. Trend Crossover Frequency (50-day MA)")
print("-"*80)
print(f"Total crossovers:")
print(f"  Pre-COVID:  {pre_crossovers} crossovers in {len(df_pre)} days ({pre_crossovers/len(df_pre)*100:.2f} per 100 days)")
print(f"  Post-COVID: {post_crossovers} crossovers in {len(df_post)} days ({post_crossovers/len(df_post)*100:.2f} per 100 days)")
print("\nInterpretation: More crossovers = less stable trend, higher whipsaw risk")

# ============================================================================
# 6. REGIME STABILITY ANALYSIS
# ============================================================================

print("\n\n" + "="*80)
print("6. MARKET REGIME STABILITY ANALYSIS")
print("="*80)

# Define regime: High volatility vs Low volatility
pre_vol_median = df_pre['vol_20d'].median()
post_vol_median = df_post['vol_20d'].median()

df_pre['high_vol_regime'] = df_pre['vol_20d'] > pre_vol_median
df_post['high_vol_regime'] = df_post['vol_20d'] > post_vol_median

# Regime persistence: How many consecutive days in same regime
def regime_persistence(regime_series):
    regime_changes = regime_series.diff().fillna(False).astype(bool)
    regime_lengths = []
    current_length = 1
    
    for changed in regime_changes:
        if changed:
            regime_lengths.append(current_length)
            current_length = 1
        else:
            current_length += 1
    regime_lengths.append(current_length)
    
    return np.mean(regime_lengths)

pre_persistence = regime_persistence(df_pre['high_vol_regime'])
post_persistence = regime_persistence(df_post['high_vol_regime'])

# High volatility regime frequency
pre_high_vol_freq = df_pre['high_vol_regime'].mean()
post_high_vol_freq = df_post['high_vol_regime'].mean()

print("\nA. Regime Frequency (High Volatility > Median)")
print("-"*80)
print(f"Pre-COVID:  {pre_high_vol_freq:.2%} of days")
print(f"Post-COVID: {post_high_vol_freq:.2%} of days")

print("\nB. Regime Persistence (Average Consecutive Days in Same Regime)")
print("-"*80)
print(f"Pre-COVID:  {pre_persistence:.1f} days average")
print(f"Post-COVID: {post_persistence:.1f} days average")
print(f"Change:     {(post_persistence - pre_persistence):+.1f} days")
print("\nInterpretation: Lower persistence = more frequent regime switches (less stability)")

# Coefficient of variation for volatility
pre_vol_cv = df_pre['vol_20d'].std() / df_pre['vol_20d'].mean()
post_vol_cv = df_post['vol_20d'].std() / df_post['vol_20d'].mean()

print("\nC. Volatility Stability (Coefficient of Variation)")
print("-"*80)
print(f"Pre-COVID:  {pre_vol_cv:.4f}")
print(f"Post-COVID: {post_vol_cv:.4f}")
print(f"Change:     {(post_vol_cv - pre_vol_cv):+.4f}")
print("\nInterpretation: Higher CV = less stable volatility (more regime uncertainty)")

# ============================================================================
# 7. SAVE RESULTS
# ============================================================================

print("\n\n" + "="*80)
print("7. GENERATING OUTPUT FILES")
print("="*80)

import os
os.makedirs('Results_Market_Structure', exist_ok=True)

# Create comprehensive results table
results_data = {
    'Metric': [
        'Annualized Volatility',
        'Downside Volatility',
        'Volatility Clustering (ACF Lag 1)',
        'Mean Daily Return',
        'Return Skewness',
        'Return Kurtosis (Excess)',
        '5th Percentile (VaR)',
        '95th Percentile',
        'Mean Volume',
        'Volume-Volatility Correlation',
        'Volume Spike Frequency',
        'RSI Overbought Frequency',
        'RSI Oversold Frequency',
        'MA-50 Deviation (Mean)',
        'MA-50 Crossovers per 100 days',
        'High Vol Regime Frequency',
        'Regime Persistence (days)',
        'Volatility Coefficient of Variation'
    ],
    'Pre_COVID': [
        f"{pre_vol:.2%}",
        f"{pre_downside:.2%}",
        f"{pre_acf:.4f}",
        f"{pre_mean:.4%}",
        f"{pre_skew:+.4f}",
        f"{pre_kurt:+.4f}",
        f"{pre_var_5:.3%}",
        f"{pre_var_95:.3%}",
        f"{pre_vol_mean:,.0f}",
        f"{pre_vol_corr:.4f}",
        f"{pre_spike_freq:.2%}",
        f"{pre_rsi_ob:.2%}",
        f"{pre_rsi_os:.2%}",
        f"{pre_dev_mean:.3%}",
        f"{pre_crossovers/len(df_pre)*100:.2f}",
        f"{pre_high_vol_freq:.2%}",
        f"{pre_persistence:.1f}",
        f"{pre_vol_cv:.4f}"
    ],
    'Post_COVID': [
        f"{post_vol:.2%}",
        f"{post_downside:.2%}",
        f"{post_acf:.4f}",
        f"{post_mean:.4%}",
        f"{post_skew:+.4f}",
        f"{post_kurt:+.4f}",
        f"{post_var_5:.3%}",
        f"{post_var_95:.3%}",
        f"{post_vol_mean:,.0f}",
        f"{post_vol_corr:.4f}",
        f"{post_spike_freq:.2%}",
        f"{post_rsi_ob:.2%}",
        f"{post_rsi_os:.2%}",
        f"{post_dev_mean:.3%}",
        f"{post_crossovers/len(df_post)*100:.2f}",
        f"{post_high_vol_freq:.2%}",
        f"{post_persistence:.1f}",
        f"{post_vol_cv:.4f}"
    ],
    'Interpretation': [
        f"{post_vol/pre_vol:.2f}x multiplier",
        f"{(post_downside/pre_downside - 1):+.1%} change",
        f"{'Stronger' if post_acf > pre_acf else 'Weaker'} clustering",
        f"{(post_mean - pre_mean):.4%} difference",
        f"{'More negative' if post_skew < pre_skew else 'Less negative'} tail",
        f"{'Fatter' if post_kurt > pre_kurt else 'Thinner'} tails",
        f"{'Worse' if post_var_5 < pre_var_5 else 'Better'} left tail",
        f"{(post_var_95 - pre_var_95):.3%} difference",
        f"{(post_vol_mean/pre_vol_mean - 1):+.1%} change",
        f"{(post_vol_corr - pre_vol_corr):+.4f} change",
        f"{(post_spike_freq - pre_spike_freq):+.2%} pp",
        f"{(post_rsi_ob - pre_rsi_ob):+.2%} pp",
        f"{(post_rsi_os - pre_rsi_os):+.2%} pp",
        f"{(post_dev_mean - pre_dev_mean):+.3%} pp",
        f"{(post_crossovers/len(df_post) - pre_crossovers/len(df_pre))*100:+.2f} per 100 days",
        f"{(post_high_vol_freq - pre_high_vol_freq):+.2%} pp",
        f"{(post_persistence - pre_persistence):+.1f} days change",
        f"{'Less' if post_vol_cv < pre_vol_cv else 'More'} stable"
    ]
}

results_df = pd.DataFrame(results_data)
results_df.to_csv('Results_Market_Structure/market_structure_analysis.csv', index=False)
print("✓ Saved: Results_Market_Structure/market_structure_analysis.csv")

# Save statistical tests
tests_data = {
    'Test': [
        'Variance Equality (Levene)',
        'Distribution Equality (K-S)',
        'Normality Pre-COVID (Jarque-Bera)',
        'Normality Post-COVID (Jarque-Bera)'
    ],
    'Statistic': [
        f"{levene_stat:.4f}",
        f"{ks_stat:.4f}",
        f"{jb_pre_stat:.4f}",
        f"{jb_post_stat:.4f}"
    ],
    'P_Value': [
        f"{levene_p:.6f}",
        f"{ks_p:.6f}",
        f"{jb_pre_p:.6f}",
        f"{jb_post_p:.6f}"
    ],
    'Conclusion': [
        'Reject H0: Variances differ' if levene_p < 0.05 else 'Cannot reject equal variance',
        'Reject H0: Distributions differ' if ks_p < 0.05 else 'Cannot reject equal distributions',
        'Reject normality' if jb_pre_p < 0.05 else 'Cannot reject normality',
        'Reject normality' if jb_post_p < 0.05 else 'Cannot reject normality'
    ]
}

tests_df = pd.DataFrame(tests_data)
tests_df.to_csv('Results_Market_Structure/statistical_tests.csv', index=False)
print("✓ Saved: Results_Market_Structure/statistical_tests.csv")

# ============================================================================
# 8. VISUALIZATIONS
# ============================================================================

print("\n8. GENERATING VISUALIZATIONS")
print("-"*80)

# Plot 1: Volatility comparison
fig, axes = plt.subplots(2, 1, figsize=(16, 10))

axes[0].plot(df_pre['date'], df_pre['vol_20d'], color='#3498db', linewidth=1.5, alpha=0.8, label='Pre-COVID')
axes[0].axhline(y=pre_vol, color='#3498db', linestyle='--', alpha=0.5, label=f'Mean: {pre_vol:.2%}')
axes[0].set_ylabel('Annualized Volatility', fontweight='bold')
axes[0].set_title('Pre-COVID Volatility (20-Day Rolling)', fontweight='bold', fontsize=12)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(df_post['date'], df_post['vol_20d'], color='#e74c3c', linewidth=1.5, alpha=0.8, label='Post-COVID')
axes[1].axhline(y=post_vol, color='#e74c3c', linestyle='--', alpha=0.5, label=f'Mean: {post_vol:.2%}')
axes[1].set_xlabel('Date', fontweight='bold')
axes[1].set_ylabel('Annualized Volatility', fontweight='bold')
axes[1].set_title('Post-COVID Volatility (20-Day Rolling)', fontweight='bold', fontsize=12)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('NIFTY Bank Index: Realized Volatility Comparison', fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('Results_Market_Structure/volatility_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Results_Market_Structure/volatility_comparison.png")
plt.close()

# Plot 2: Return distributions
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].hist(df_pre['daily_return'].dropna(), bins=50, color='#3498db', alpha=0.7, edgecolor='black', density=True)
axes[0].axvline(x=pre_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {pre_mean:.3%}')
axes[0].set_xlabel('Daily Return', fontweight='bold')
axes[0].set_ylabel('Density', fontweight='bold')
axes[0].set_title(f'Pre-COVID Return Distribution\nSkew={pre_skew:.2f}, Kurt={pre_kurt:.2f}', fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].hist(df_post['daily_return'].dropna(), bins=50, color='#e74c3c', alpha=0.7, edgecolor='black', density=True)
axes[1].axvline(x=post_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {post_mean:.3%}')
axes[1].set_xlabel('Daily Return', fontweight='bold')
axes[1].set_ylabel('Density', fontweight='bold')
axes[1].set_title(f'Post-COVID Return Distribution\nSkew={post_skew:.2f}, Kurt={post_kurt:.2f}', fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('NIFTY Bank Index: Return Distribution Comparison', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('Results_Market_Structure/return_distributions.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Results_Market_Structure/return_distributions.png")
plt.close()

# Plot 3: Volume-Volatility relationship
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].scatter(df_pre['volume'], df_pre['abs_return'], alpha=0.3, s=20, color='#3498db')
axes[0].set_xlabel('Volume', fontweight='bold')
axes[0].set_ylabel('Absolute Return', fontweight='bold')
axes[0].set_title(f'Pre-COVID: Volume-Volatility Relationship\nCorr={pre_vol_corr:.3f}', fontweight='bold')
axes[0].grid(True, alpha=0.3)

axes[1].scatter(df_post['volume'], df_post['abs_return'], alpha=0.3, s=20, color='#e74c3c')
axes[1].set_xlabel('Volume', fontweight='bold')
axes[1].set_ylabel('Absolute Return', fontweight='bold')
axes[1].set_title(f'Post-COVID: Volume-Volatility Relationship\nCorr={post_vol_corr:.3f}', fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.suptitle('NIFTY Bank Index: Liquidity Dynamics', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('Results_Market_Structure/volume_volatility.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Results_Market_Structure/volume_volatility.png")
plt.close()

print("\n" + "="*80)
print("ANALYSIS COMPLETE - All results saved to Results_Market_Structure/")
print("="*80)
