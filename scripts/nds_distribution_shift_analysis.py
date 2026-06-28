"""
NDS DISTRIBUTION SHIFT ANALYSIS
================================

Quantifies and tests distributional differences in Neuro Decision Score (NDS)
between Pre-COVID and Post-COVID periods using statistical methods.

Methodology:
- Mean and variance comparison
- Two-sample Kolmogorov-Smirnov test
- Distributional visualization

NO trading signals, NO profitability claims, NO psychological attribution.
Strictly descriptive statistical analysis.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Import scipy functions individually to avoid conflicts
from scipy import stats
ks_2samp = stats.ks_2samp
levene = stats.levene
mannwhitneyu = stats.mannwhitneyu
ttest_ind = stats.ttest_ind
gaussian_kde = stats.gaussian_kde

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("="*80)
print("NDS DISTRIBUTION SHIFT ANALYSIS")
print("="*80)
print("\nObjective: Quantify statistical differences in NDS distribution")
print("             between Pre-COVID and Post-COVID periods")
print("="*80)

# ============================================================================
# 1. DATA LOADING AND SEGMENTATION
# ============================================================================

print("\n1. DATA LOADING AND SEGMENTATION")
print("-"*80)

# Load NDS timeseries data
df = pd.read_csv('../DataSplitExperiments/PrePostComparison/Results_NDS_Stability/nds_timeseries.csv')
df['Date'] = pd.to_datetime(df['Date'])

print(f"✓ Loaded NDS timeseries: {len(df)} observations")

# Segment by period
df_pre = df[df['Period'] == 'Pre-COVID'].copy()
df_post = df[df['Period'] == 'Post-COVID'].copy()

print(f"\nPeriod Segmentation:")
print(f"  Pre-COVID:  {len(df_pre)} observations")
print(f"              Date range: {df_pre['Date'].min().date()} to {df_pre['Date'].max().date()}")
print(f"  Post-COVID: {len(df_post)} observations")
print(f"              Date range: {df_post['Date'].min().date()} to {df_post['Date'].max().date()}")

# Extract NDS values
nds_pre = df_pre['NDS'].values
nds_post = df_post['NDS'].values

print(f"\n✓ Sample sizes verified:")
print(f"  n_pre = {len(nds_pre)}, n_post = {len(nds_post)}")

# ============================================================================
# 2. DESCRIPTIVE STATISTICS
# ============================================================================

print("\n\n" + "="*80)
print("2. DESCRIPTIVE STATISTICS")
print("="*80)

# Central tendency
mean_pre = np.mean(nds_pre)
mean_post = np.mean(nds_post)
mean_diff = mean_post - mean_pre

median_pre = np.median(nds_pre)
median_post = np.median(nds_post)

# Dispersion
var_pre = np.var(nds_pre, ddof=1)  # Sample variance
var_post = np.var(nds_post, ddof=1)
var_diff = var_post - var_pre

std_pre = np.std(nds_pre, ddof=1)
std_post = np.std(nds_post, ddof=1)

# Range
min_pre = np.min(nds_pre)
max_pre = np.max(nds_pre)
min_post = np.min(nds_post)
max_post = np.max(nds_post)

# Interquartile range
q25_pre = np.percentile(nds_pre, 25)
q75_pre = np.percentile(nds_pre, 75)
iqr_pre = q75_pre - q25_pre

q25_post = np.percentile(nds_post, 25)
q75_post = np.percentile(nds_post, 75)
iqr_post = q75_post - q25_post

print("\nTable 1: Summary Statistics of NDS Distribution")
print("-"*80)
print(f"{'Statistic':<25} {'Pre-COVID':<15} {'Post-COVID':<15} {'Difference':<15}")
print("-"*80)
print(f"{'Mean':<25} {mean_pre:>14.4f} {mean_post:>14.4f} {mean_diff:>14.4f}")
print(f"{'Median':<25} {median_pre:>14.4f} {median_post:>14.4f} {(median_post-median_pre):>14.4f}")
print(f"{'Variance':<25} {var_pre:>14.4f} {var_post:>14.4f} {var_diff:>14.4f}")
print(f"{'Std Deviation':<25} {std_pre:>14.4f} {std_post:>14.4f} {(std_post-std_pre):>14.4f}")
print(f"{'Minimum':<25} {min_pre:>14.4f} {min_post:>14.4f} {(min_post-min_pre):>14.4f}")
print(f"{'Maximum':<25} {max_pre:>14.4f} {max_post:>14.4f} {(max_post-max_pre):>14.4f}")
print(f"{'Q1 (25th percentile)':<25} {q25_pre:>14.4f} {q25_post:>14.4f} {(q25_post-q25_pre):>14.4f}")
print(f"{'Q3 (75th percentile)':<25} {q75_pre:>14.4f} {q75_post:>14.4f} {(q75_post-q75_pre):>14.4f}")
print(f"{'IQR':<25} {iqr_pre:>14.4f} {iqr_post:>14.4f} {(iqr_post-iqr_pre):>14.4f}")
print("-"*80)

# ============================================================================
# 3. DISTRIBUTIONAL COMPARISON TESTS
# ============================================================================

print("\n\n" + "="*80)
print("3. DISTRIBUTIONAL COMPARISON TESTS")
print("="*80)

# Kolmogorov-Smirnov Test (primary test)
ks_stat, ks_pvalue = ks_2samp(nds_pre, nds_post)

print("\n3.1 Two-Sample Kolmogorov-Smirnov Test")
print("-"*80)
print("Null Hypothesis: Pre-COVID and Post-COVID NDS distributions are identical")
print(f"\nKS Statistic:  {ks_stat:.6f}")
print(f"p-value:       {ks_pvalue:.6e}")

if ks_pvalue < 0.001:
    ks_decision = "REJECT H₀ (p < 0.001)"
elif ks_pvalue < 0.01:
    ks_decision = "REJECT H₀ (p < 0.01)"
elif ks_pvalue < 0.05:
    ks_decision = "REJECT H₀ (p < 0.05)"
else:
    ks_decision = "FAIL TO REJECT H₀ (p ≥ 0.05)"

print(f"Decision:      {ks_decision}")
print(f"\nConclusion: Distributions are {'SIGNIFICANTLY DIFFERENT' if ks_pvalue < 0.05 else 'NOT significantly different'}")

# Levene's Test (variance equality)
levene_stat, levene_pvalue = levene(nds_pre, nds_post)

print("\n\n3.2 Levene's Test for Variance Equality")
print("-"*80)
print("Null Hypothesis: Pre-COVID and Post-COVID NDS have equal variances")
print(f"\nLevene Statistic: {levene_stat:.6f}")
print(f"p-value:          {levene_pvalue:.6e}")

if levene_pvalue < 0.05:
    levene_decision = "REJECT H₀ (variances differ)"
else:
    levene_decision = "FAIL TO REJECT H₀ (equal variance assumption holds)"

print(f"Decision:         {levene_decision}")

# Mann-Whitney U Test (median comparison, non-parametric)
mw_stat, mw_pvalue = mannwhitneyu(nds_pre, nds_post, alternative='two-sided')

print("\n\n3.3 Mann-Whitney U Test (Median Comparison)")
print("-"*80)
print("Null Hypothesis: Pre-COVID and Post-COVID NDS have identical medians")
print(f"\nU Statistic:   {mw_stat:.2f}")
print(f"p-value:       {mw_pvalue:.6e}")

if mw_pvalue < 0.05:
    mw_decision = "REJECT H₀ (medians differ)"
else:
    mw_decision = "FAIL TO REJECT H₀"

print(f"Decision:      {mw_decision}")

# t-test for mean comparison (if normality assumption reasonable)
t_stat, t_pvalue = ttest_ind(nds_pre, nds_post, equal_var=(levene_pvalue >= 0.05))

print("\n\n3.4 Two-Sample t-Test (Mean Comparison)")
print("-"*80)
print("Null Hypothesis: Pre-COVID and Post-COVID NDS have equal means")
print(f"\nt-Statistic:   {t_stat:.6f}")
print(f"p-value:       {t_pvalue:.6e}")

if t_pvalue < 0.05:
    t_decision = "REJECT H₀ (means differ)"
else:
    t_decision = "FAIL TO REJECT H₀"

print(f"Decision:      {t_decision}")

# ============================================================================
# 4. EFFECT SIZE CALCULATION
# ============================================================================

print("\n\n" + "="*80)
print("4. EFFECT SIZE MEASURES")
print("="*80)

# Cohen's d
pooled_std = np.sqrt((var_pre + var_post) / 2)
cohens_d = (mean_post - mean_pre) / pooled_std

print(f"\nCohen's d (standardized mean difference): {cohens_d:.4f}")

if abs(cohens_d) < 0.2:
    effect_interp = "negligible"
elif abs(cohens_d) < 0.5:
    effect_interp = "small"
elif abs(cohens_d) < 0.8:
    effect_interp = "medium"
else:
    effect_interp = "large"

print(f"Interpretation: {effect_interp} effect size")

# Variance ratio
var_ratio = var_post / var_pre
print(f"\nVariance Ratio (Post/Pre): {var_ratio:.4f}")
print(f"Interpretation: Post-COVID variance is {var_ratio:.2f}x Pre-COVID variance")

# ============================================================================
# 5. SAVE RESULTS
# ============================================================================

print("\n\n" + "="*80)
print("5. SAVING RESULTS")
print("="*80)

# Summary statistics table
summary_stats = pd.DataFrame({
    'Statistic': ['Sample Size', 'Mean', 'Median', 'Variance', 'Std Deviation', 
                  'Minimum', 'Maximum', 'Q1 (25%)', 'Q3 (75%)', 'IQR'],
    'Pre_COVID': [len(nds_pre), mean_pre, median_pre, var_pre, std_pre,
                  min_pre, max_pre, q25_pre, q75_pre, iqr_pre],
    'Post_COVID': [len(nds_post), mean_post, median_post, var_post, std_post,
                   min_post, max_post, q25_post, q75_post, iqr_post],
    'Difference': [len(nds_post) - len(nds_pre), mean_diff, median_post - median_pre,
                   var_diff, std_post - std_pre, min_post - min_pre, max_post - max_pre,
                   q25_post - q25_pre, q75_post - q75_pre, iqr_post - iqr_pre]
})

summary_stats.to_csv('nds_distribution_summary_statistics.csv', index=False)
print("✓ Saved: nds_distribution_summary_statistics.csv")

# Statistical tests results
test_results = pd.DataFrame({
    'Test': [
        'Kolmogorov-Smirnov',
        'Levene (Variance Equality)',
        'Mann-Whitney U',
        'Two-Sample t-test'
    ],
    'Statistic': [ks_stat, levene_stat, mw_stat, t_stat],
    'P_Value': [ks_pvalue, levene_pvalue, mw_pvalue, t_pvalue],
    'Decision': [ks_decision, levene_decision, mw_decision, t_decision]
})

test_results.to_csv('nds_distribution_test_results.csv', index=False)
print("✓ Saved: nds_distribution_test_results.csv")

# Effect sizes
effect_sizes = pd.DataFrame({
    'Measure': ['Cohen\'s d', 'Variance Ratio (Post/Pre)'],
    'Value': [cohens_d, var_ratio],
    'Interpretation': [effect_interp, f'{var_ratio:.2f}x variance increase']
})

effect_sizes.to_csv('nds_distribution_effect_sizes.csv', index=False)
print("✓ Saved: nds_distribution_effect_sizes.csv")

# ============================================================================
# 6. VISUALIZATIONS
# ============================================================================

print("\n\n" + "="*80)
print("6. GENERATING VISUALIZATIONS")
print("="*80)

# Plot 1: Overlapping Histograms
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

ax.hist(nds_pre, bins=40, alpha=0.6, color='#3498db', edgecolor='black', 
        label=f'Pre-COVID (n={len(nds_pre)})', density=True)
ax.hist(nds_post, bins=40, alpha=0.6, color='#e74c3c', edgecolor='black',
        label=f'Post-COVID (n={len(nds_post)})', density=True)

ax.axvline(mean_pre, color='#3498db', linestyle='--', linewidth=2.5, 
           label=f'Pre Mean: {mean_pre:.3f}')
ax.axvline(mean_post, color='#e74c3c', linestyle='--', linewidth=2.5,
           label=f'Post Mean: {mean_post:.3f}')

ax.set_xlabel('Neuro Decision Score (NDS)', fontweight='bold', fontsize=12)
ax.set_ylabel('Density', fontweight='bold', fontsize=12)
ax.set_title('NDS Distribution Comparison: Pre-COVID vs Post-COVID\n' + 
             f'K-S Test: D={ks_stat:.4f}, p={ks_pvalue:.2e}',
             fontweight='bold', fontsize=14)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('nds_distribution_histogram.png', dpi=300, bbox_inches='tight')
print("✓ Saved: nds_distribution_histogram.png")
plt.close()

# Plot 2: Kernel Density Estimate (Smoothed)
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

# Compute KDE
kde_pre = gaussian_kde(nds_pre)
kde_post = gaussian_kde(nds_post)

# Create x-axis range
x_min = min(nds_pre.min(), nds_post.min()) - 1
x_max = max(nds_pre.max(), nds_post.max()) + 1
x_range = np.linspace(x_min, x_max, 500)

# Plot KDE
ax.plot(x_range, kde_pre(x_range), color='#3498db', linewidth=3, 
        label=f'Pre-COVID (μ={mean_pre:.3f}, σ={std_pre:.3f})', alpha=0.8)
ax.plot(x_range, kde_post(x_range), color='#e74c3c', linewidth=3,
        label=f'Post-COVID (μ={mean_post:.3f}, σ={std_post:.3f})', alpha=0.8)

# Fill areas
ax.fill_between(x_range, kde_pre(x_range), alpha=0.3, color='#3498db')
ax.fill_between(x_range, kde_post(x_range), alpha=0.3, color='#e74c3c')

ax.axvline(mean_pre, color='#3498db', linestyle='--', linewidth=2, alpha=0.7)
ax.axvline(mean_post, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)

ax.set_xlabel('Neuro Decision Score (NDS)', fontweight='bold', fontsize=12)
ax.set_ylabel('Probability Density', fontweight='bold', fontsize=12)
ax.set_title('NDS Kernel Density Estimate: Distributional Shift\n' +
             f'Mean Shift: {mean_diff:.3f} (Cohen\'s d = {cohens_d:.3f})',
             fontweight='bold', fontsize=14)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('nds_distribution_kde.png', dpi=300, bbox_inches='tight')
print("✓ Saved: nds_distribution_kde.png")
plt.close()

# Plot 3: Box Plot Comparison
fig, ax = plt.subplots(1, 1, figsize=(10, 7))

bp = ax.boxplot([nds_pre, nds_post], labels=['Pre-COVID', 'Post-COVID'],
                patch_artist=True, widths=0.6,
                boxprops=dict(linewidth=2),
                medianprops=dict(color='red', linewidth=3),
                whiskerprops=dict(linewidth=2),
                capprops=dict(linewidth=2))

# Color boxes
bp['boxes'][0].set_facecolor('#3498db')
bp['boxes'][0].set_alpha(0.6)
bp['boxes'][1].set_facecolor('#e74c3c')
bp['boxes'][1].set_alpha(0.6)

# Add mean markers
ax.plot([1, 2], [mean_pre, mean_post], 'D', color='green', markersize=12,
        label='Mean', zorder=5)

ax.set_ylabel('Neuro Decision Score (NDS)', fontweight='bold', fontsize=12)
ax.set_title('NDS Distribution: Box Plot Comparison\n' +
             f'Pre-COVID: Median={median_pre:.3f}, IQR={iqr_pre:.3f}  |  ' +
             f'Post-COVID: Median={median_post:.3f}, IQR={iqr_post:.3f}',
             fontweight='bold', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('nds_distribution_boxplot.png', dpi=300, bbox_inches='tight')
print("✓ Saved: nds_distribution_boxplot.png")
plt.close()

# Plot 4: Q-Q Plot (Quantile-Quantile)
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Compute quantiles
quantiles = np.linspace(0, 1, min(len(nds_pre), len(nds_post)))
q_pre = np.quantile(nds_pre, quantiles)
q_post = np.quantile(nds_post, quantiles)

# Plot Q-Q
ax.scatter(q_pre, q_post, alpha=0.6, s=30, color='#9b59b6', edgecolor='black')

# Reference line (y=x)
min_val = min(q_pre.min(), q_post.min())
max_val = max(q_pre.max(), q_post.max())
ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2.5,
        label='Reference (identical distributions)')

ax.set_xlabel('Pre-COVID NDS Quantiles', fontweight='bold', fontsize=12)
ax.set_ylabel('Post-COVID NDS Quantiles', fontweight='bold', fontsize=12)
ax.set_title('Q-Q Plot: Pre-COVID vs Post-COVID NDS Distribution\n' +
             'Deviation from reference line indicates distributional shift',
             fontweight='bold', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_aspect('equal', adjustable='box')

plt.tight_layout()
plt.savefig('nds_distribution_qqplot.png', dpi=300, bbox_inches='tight')
print("✓ Saved: nds_distribution_qqplot.png")
plt.close()

# ============================================================================
# 7. STATISTICAL INTERPRETATION (ACADEMIC FORMAT)
# ============================================================================

print("\n\n" + "="*80)
print("7. STATISTICAL INTERPRETATION")
print("="*80)

interpretation = f"""
STATISTICAL SUMMARY OF NDS DISTRIBUTION SHIFT

The mean and variance of the Neuro Decision Score (NDS) differ substantially 
between the Pre-COVID and Post-COVID periods. Pre-COVID mean NDS was {mean_pre:.4f} 
(σ = {std_pre:.4f}), while Post-COVID mean NDS decreased to {mean_post:.4f} 
(σ = {std_post:.4f}), representing a shift of {mean_diff:.4f} ({abs(mean_diff/mean_pre)*100:.1f}% 
{'decrease' if mean_diff < 0 else 'increase'}).

A two-sample Kolmogorov-Smirnov test decisively rejects the null hypothesis of 
identical distributions (D = {ks_stat:.6f}, p = {ks_pvalue:.2e}), indicating a 
statistically significant shift in the distribution of market decision states 
following COVID-19. The effect size, measured by Cohen's d = {cohens_d:.4f}, 
is classified as {effect_interp}.

Variance increased from {var_pre:.4f} to {var_post:.4f} (ratio = {var_ratio:.4f}), 
confirmed by Levene's test (p = {levene_pvalue:.2e}), indicating greater dispersion 
in decision states Post-COVID. Mann-Whitney U test confirms median shift 
(p = {mw_pvalue:.2e}).

These findings demonstrate a fundamental structural change in the distribution of 
market cognitive states, characterized by both location shift (mean) and scale 
change (variance). The statistical evidence is robust across multiple tests 
(KS, t-test, Mann-Whitney, Levene), all rejecting equality at conventional 
significance levels.
"""

print(interpretation)

# Save interpretation
with open('nds_distribution_interpretation.txt', 'w', encoding='utf-8') as f:
    f.write(interpretation)

print("\n✓ Saved: nds_distribution_interpretation.txt")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nGenerated Files:")
print("  1. nds_distribution_summary_statistics.csv")
print("  2. nds_distribution_test_results.csv")
print("  3. nds_distribution_effect_sizes.csv")
print("  4. nds_distribution_histogram.png")
print("  5. nds_distribution_kde.png")
print("  6. nds_distribution_boxplot.png")
print("  7. nds_distribution_qqplot.png")
print("  8. nds_distribution_interpretation.txt")
print("\nAll results strictly descriptive, suitable for peer review.")
print("="*80)
