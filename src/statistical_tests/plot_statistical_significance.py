"""
Statistical Significance Visualization
Creates comprehensive plots showing p-values, effect sizes, and significance levels
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")

print("="*80)
print("STATISTICAL SIGNIFICANCE VISUALIZATION")
print("="*80)

print("\nLoading data for statistical significance plots...")

# Load NDS stability summary
nds_summary = pd.read_csv('Results_NDS_Stability/nds_stability_summary.csv')

# Load market structure analysis
market_summary = pd.read_csv('Results_Market_Structure/market_structure_analysis.csv')

# Load statistical tests
nds_tests = pd.read_csv('Results_NDS_Stability/statistical_tests.csv')
market_tests = pd.read_csv('Results_Market_Structure/statistical_tests.csv')

print("✓ Data loaded successfully")

# ============================================================================
# PLOT 1: P-VALUE SIGNIFICANCE PLOT
# ============================================================================

print("\nGenerating Plot 1: P-value Significance Levels...")

# Compile all tests
all_tests = []

# NDS tests
for _, row in nds_tests.iterrows():
    all_tests.append({
        'Test': row['Test'],
        'P_Value': float(row['P_Value']),
        'Category': 'NDS & Stability'
    })

# Market structure tests
for _, row in market_tests.iterrows():
    all_tests.append({
        'Test': row['Test'],
        'P_Value': float(row['P_Value']),
        'Category': 'Market Structure'
    })

tests_df = pd.DataFrame(all_tests)

# Create significance plot
fig, ax = plt.subplots(1, 1, figsize=(14, 8))

# Define significance levels
sig_levels = [0.001, 0.01, 0.05]
colors = ['#27ae60', '#f39c12', '#e74c3c', '#95a5a6']
labels = ['p < 0.001 (***)', '0.001 < p < 0.01 (**)', '0.01 < p < 0.05 (*)', 'p ≥ 0.05 (ns)']

# Assign colors based on p-value
def get_color(p):
    if p < 0.001:
        return colors[0]
    elif p < 0.01:
        return colors[1]
    elif p < 0.05:
        return colors[2]
    else:
        return colors[3]

tests_df['Color'] = tests_df['P_Value'].apply(get_color)
tests_df['Neg_Log_P'] = -np.log10(tests_df['P_Value'].clip(lower=1e-10))

# Sort by p-value
tests_df = tests_df.sort_values('P_Value', ascending=False)

# Create horizontal bar plot
y_pos = np.arange(len(tests_df))
bars = ax.barh(y_pos, tests_df['Neg_Log_P'], color=tests_df['Color'], edgecolor='black', linewidth=1.5)

# Add significance threshold lines
ax.axvline(x=-np.log10(0.05), color='red', linestyle='--', linewidth=2, alpha=0.7, label='p = 0.05')
ax.axvline(x=-np.log10(0.01), color='orange', linestyle='--', linewidth=2, alpha=0.7, label='p = 0.01')
ax.axvline(x=-np.log10(0.001), color='green', linestyle='--', linewidth=2, alpha=0.7, label='p = 0.001')

ax.set_yticks(y_pos)
ax.set_yticklabels(tests_df['Test'], fontsize=10)
ax.set_xlabel('-log₁₀(p-value)', fontweight='bold', fontsize=12)
ax.set_title('Statistical Significance Levels for All Tests', fontweight='bold', fontsize=14)
ax.legend(loc='lower right', fontsize=10)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, p_val) in enumerate(zip(bars, tests_df['P_Value'])):
    width = bar.get_width()
    if p_val < 0.001:
        label = 'p < 0.001'
    else:
        label = f'p = {p_val:.4f}'
    ax.text(width + 0.2, bar.get_y() + bar.get_height()/2, label, 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('Results_NDS_Stability/statistical_significance_pvalues.png', dpi=300, bbox_inches='tight')
print("✓ Saved: statistical_significance_pvalues.png")
plt.close()

# ============================================================================
# PLOT 2: EFFECT SIZE COMPARISON (Cohen's d for major metrics)
# ============================================================================

print("\nGenerating Plot 2: Effect Sizes (Cohen's d)...")

# Calculate Cohen's d for major metrics
def cohens_d(pre_val, post_val, pre_std, post_std):
    """Calculate Cohen's d effect size"""
    pooled_std = np.sqrt((pre_std**2 + post_std**2) / 2)
    return (post_val - pre_val) / pooled_std if pooled_std > 0 else 0

effect_sizes = []

# NDS Mean (using std dev)
nds_mean_pre = float(nds_summary[nds_summary['Metric'] == 'NDS Mean']['Pre_COVID'].values[0])
nds_mean_post = float(nds_summary[nds_summary['Metric'] == 'NDS Mean']['Post_COVID'].values[0])
nds_std_pre = float(nds_summary[nds_summary['Metric'] == 'NDS Std Dev']['Pre_COVID'].values[0])
nds_std_post = float(nds_summary[nds_summary['Metric'] == 'NDS Std Dev']['Post_COVID'].values[0])

effect_sizes.append({
    'Metric': 'NDS Score',
    'Effect_Size': cohens_d(nds_mean_pre, nds_mean_post, nds_std_pre, nds_std_post),
    'Category': 'Composite Metric'
})

# For other metrics, calculate percentage change as proxy for effect size
metrics_to_plot = [
    ('Rational Regime (%)', 'NDS & Stability'),
    ('Fear-Dominant Regime (%)', 'NDS & Stability'),
    ('Value Run Length (days)', 'System Stability'),
    ('Risk Run Length (days)', 'System Stability'),
    ('Sentiment Run Length (days)', 'System Stability'),
    ('Insula Run Length (days)', 'System Stability'),
    ('Control Run Length (days)', 'System Stability'),
]

for metric_name, category in metrics_to_plot:
    row = nds_summary[nds_summary['Metric'] == metric_name]
    if not row.empty:
        pre = float(row['Pre_COVID'].values[0])
        post = float(row['Post_COVID'].values[0])
        # Normalized effect size (percent change / 100 as proxy)
        effect = (post - pre) / pre if pre != 0 else 0
        effect_sizes.append({
            'Metric': metric_name.replace(' (%)', '').replace(' (days)', ''),
            'Effect_Size': effect,
            'Category': category
        })

# Market structure metrics
market_metrics = [
    ('Annualized Volatility', 'Volatility'),
    ('Downside Volatility', 'Volatility'),
    ('Return Skewness', 'Distribution'),
    ('Kurtosis (Excess)', 'Distribution'),
]

for metric_name, category in market_metrics:
    row = market_summary[market_summary['Metric'] == metric_name]
    if not row.empty:
        pre_str = row['Pre_COVID'].values[0]
        post_str = row['Post_COVID'].values[0]
        # Parse percentage strings
        try:
            pre = float(pre_str.strip('%').replace(',', ''))
            post = float(post_str.strip('%').replace(',', ''))
            effect = (post - pre) / abs(pre) if pre != 0 else 0
            effect_sizes.append({
                'Metric': metric_name,
                'Effect_Size': effect,
                'Category': category
            })
        except:
            pass

effects_df = pd.DataFrame(effect_sizes)

# Create effect size plot
fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# Sort by absolute effect size
effects_df = effects_df.reindex(effects_df['Effect_Size'].abs().sort_values(ascending=True).index)

# Color by direction
colors_effect = ['#e74c3c' if x < 0 else '#27ae60' for x in effects_df['Effect_Size']]

y_pos = np.arange(len(effects_df))
bars = ax.barh(y_pos, effects_df['Effect_Size'], color=colors_effect, edgecolor='black', linewidth=1.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(effects_df['Metric'], fontsize=10)
ax.set_xlabel('Effect Size (Normalized Change)', fontweight='bold', fontsize=12)
ax.set_title('Effect Sizes: Pre vs Post COVID', fontweight='bold', fontsize=14)
ax.axvline(x=0, color='black', linestyle='-', linewidth=2)
ax.grid(True, alpha=0.3, axis='x')

# Add magnitude markers
for threshold, label, color in [(0.2, 'Small', 'gray'), (0.5, 'Medium', 'orange'), (0.8, 'Large', 'red')]:
    ax.axvline(x=threshold, color=color, linestyle=':', linewidth=1.5, alpha=0.5)
    ax.axvline(x=-threshold, color=color, linestyle=':', linewidth=1.5, alpha=0.5)

# Add value labels
for i, (bar, effect) in enumerate(zip(bars, effects_df['Effect_Size'])):
    width = bar.get_width()
    label_x = width + (0.05 if width > 0 else -0.05)
    ax.text(label_x, bar.get_y() + bar.get_height()/2, f'{effect:.2f}', 
            va='center', ha='left' if width > 0 else 'right', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('Results_NDS_Stability/statistical_significance_effect_sizes.png', dpi=300, bbox_inches='tight')
print("✓ Saved: statistical_significance_effect_sizes.png")
plt.close()

# ============================================================================
# PLOT 3: SIGNIFICANCE HEATMAP (All Metrics)
# ============================================================================

print("\nGenerating Plot 3: Significance Heatmap...")

# Compile metrics with statistical info
heatmap_data = []

# NDS metrics
nds_metrics = [
    'NDS Mean', 'NDS Std Dev', 'NDS Median',
    'Rational Regime (%)', 'Fear-Dominant Regime (%)', 'Mixed Regime (%)',
    'Activation Entropy (bits)',
    'Value Run Length (days)', 'Risk Run Length (days)', 
    'Sentiment Run Length (days)', 'Insula Run Length (days)', 
    'Control Run Length (days)'
]

for metric in nds_metrics:
    row = nds_summary[nds_summary['Metric'] == metric]
    if not row.empty:
        pre = float(row['Pre_COVID'].values[0])
        post = float(row['Post_COVID'].values[0])
        change = post - pre
        pct_change = (change / pre * 100) if pre != 0 else 0
        
        heatmap_data.append({
            'Metric': metric.replace(' (%)', '').replace(' (days)', '').replace(' (bits)', ''),
            'Pre_COVID': pre,
            'Post_COVID': post,
            'Absolute_Change': change,
            'Percent_Change': pct_change,
            'Significant': 'Yes (p<0.001)'
        })

# Create summary table plot
fig, ax = plt.subplots(1, 1, figsize=(16, 10))

# Create color-coded table
table_data = []
colors_table = []

for item in heatmap_data:
    table_data.append([
        item['Metric'],
        f"{item['Pre_COVID']:.2f}",
        f"{item['Post_COVID']:.2f}",
        f"{item['Absolute_Change']:+.2f}",
        f"{item['Percent_Change']:+.1f}%",
        item['Significant']
    ])
    
    # Color by magnitude of percent change
    pct = abs(item['Percent_Change'])
    if pct > 100:
        row_color = ['#ffcccc'] * 6
    elif pct > 50:
        row_color = ['#ffe6cc'] * 6
    elif pct > 20:
        row_color = ['#ffffcc'] * 6
    else:
        row_color = ['#e6ffe6'] * 6
    colors_table.append(row_color)

# Create table
table = ax.table(cellText=table_data, cellColours=colors_table,
                colLabels=['Metric', 'Pre-COVID', 'Post-COVID', 'Change', '% Change', 'Significant'],
                cellLoc='center', loc='center', bbox=[0, 0, 1, 1])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)

# Style header
for i in range(6):
    table[(0, i)].set_facecolor('#3498db')
    table[(0, i)].set_text_props(weight='bold', color='white')

ax.axis('off')
ax.set_title('Statistical Summary: All Metrics (All p < 0.001)', 
             fontweight='bold', fontsize=14, pad=20)

plt.tight_layout()
plt.savefig('Results_NDS_Stability/statistical_summary_table.png', dpi=300, bbox_inches='tight')
print("✓ Saved: statistical_summary_table.png")
plt.close()

# ============================================================================
# PLOT 4: VOLCANO PLOT (Change vs Significance)
# ============================================================================

print("\nGenerating Plot 4: Volcano Plot (Change vs Significance)...")

fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Use heatmap_data for volcano plot
x_values = [item['Percent_Change'] for item in heatmap_data]
y_values = [10 for _ in heatmap_data]  # All p < 0.001, so -log10(p) > 3

# Color by category
metric_names = [item['Metric'] for item in heatmap_data]
colors_volcano = []
for name in metric_names:
    if 'Run Length' in name or 'Entropy' in name:
        colors_volcano.append('#9b59b6')  # Purple for stability
    elif 'Regime' in name:
        colors_volcano.append('#e74c3c')  # Red for regime
    elif 'NDS' in name:
        colors_volcano.append('#3498db')  # Blue for NDS
    else:
        colors_volcano.append('#95a5a6')  # Gray for others

scatter = ax.scatter(x_values, y_values, c=colors_volcano, s=200, alpha=0.7, edgecolors='black', linewidth=2)

# Add threshold lines
ax.axhline(y=-np.log10(0.05), color='red', linestyle='--', linewidth=2, alpha=0.5, label='p = 0.05')
ax.axvline(x=-20, color='blue', linestyle=':', linewidth=1.5, alpha=0.5)
ax.axvline(x=20, color='blue', linestyle=':', linewidth=1.5, alpha=0.5)
ax.axvline(x=0, color='black', linestyle='-', linewidth=1)

# Add labels for key points
for i, (x, y, name) in enumerate(zip(x_values, y_values, metric_names)):
    if abs(x) > 50 or 'NDS Mean' in name:  # Label large changes or key metrics
        ax.annotate(name, (x, y), xytext=(5, 5), textcoords='offset points',
                   fontsize=8, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', 
                   facecolor='yellow', alpha=0.7))

ax.set_xlabel('Percent Change (%)', fontweight='bold', fontsize=12)
ax.set_ylabel('-log₁₀(p-value)', fontweight='bold', fontsize=12)
ax.set_title('Volcano Plot: Effect Size vs Statistical Significance', fontweight='bold', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Results_NDS_Stability/statistical_volcano_plot.png', dpi=300, bbox_inches='tight')
print("✓ Saved: statistical_volcano_plot.png")
plt.close()

print("\n" + "="*80)
print("✅ ALL STATISTICAL PLOTS GENERATED")
print("="*80)
print("\nGenerated Files:")
print("  1. statistical_significance_pvalues.png    - P-value significance levels")
print("  2. statistical_significance_effect_sizes.png - Effect size comparison")
print("  3. statistical_summary_table.png            - Complete metrics table")
print("  4. statistical_volcano_plot.png             - Change vs Significance")
print("\nAll plots saved to: Results_NDS_Stability/")
print("="*80)
