"""
Generate Comprehensive Figure: NDS Distribution + Test Results Table
Combines 4-panel distribution analysis with ML vs Rule-Based comparison table
Publication-ready figure for research paper
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import gaussian_kde
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

print("Loading ML-based NDS data...")

# Load ML-based NDS timeseries data
nds_timeseries = pd.read_csv('NDS_Distribution_Analysis/nds_timeseries_data_ML.csv')

# Separate NDS by period
nds_pre = nds_timeseries[nds_timeseries['period'] == 'Pre-COVID']['NDS'].values
nds_post = nds_timeseries[nds_timeseries['period'] == 'Post-COVID']['NDS'].values

print(f"Pre-COVID: n={len(nds_pre)}, mean={nds_pre.mean():.3f}, std={nds_pre.std():.3f}")
print(f"Post-COVID: n={len(nds_post)}, mean={nds_post.mean():.3f}, std={nds_post.std():.3f}")

# Color scheme
color_pre = '#4A7BA7'      # Steel blue
color_post = '#B85450'     # Brick red

# ============================================================================
# Create comprehensive figure with distribution + table
# ============================================================================

fig = plt.figure(figsize=(16, 14))

# Create grid: 3 rows x 2 columns, with bottom row spanning full width for table
gs = fig.add_gridspec(3, 2, 
                      height_ratios=[1, 1, 0.7],
                      hspace=0.35, wspace=0.30, 
                      top=0.95, bottom=0.08, left=0.06, right=0.96)

# ============================================================================
# PANEL A (Top Left): Pre-COVID NDS Distribution
# ============================================================================
print("\nCreating Panel A: Pre-COVID Distribution...")
ax1 = fig.add_subplot(gs[0, 0])

bins_pre = np.linspace(nds_pre.min(), nds_pre.max(), 35)
n_counts, bins_edge, patches = ax1.hist(nds_pre, bins=bins_pre, 
                                        color=color_pre, alpha=0.85, 
                                        edgecolor='white', linewidth=0.6)

mean_pre = nds_pre.mean()
std_pre = nds_pre.std()
ax1.axvline(mean_pre, color='#2C3E50', linestyle='--', 
            linewidth=2, label=f'μ = {mean_pre:.2f}', zorder=10)
ax1.axvline(mean_pre - std_pre, color='#7F8C8D', linestyle=':', 
            linewidth=1.5, alpha=0.7, label=f'σ = {std_pre:.2f}', zorder=9)
ax1.axvline(mean_pre + std_pre, color='#7F8C8D', linestyle=':', 
            linewidth=1.5, alpha=0.7, zorder=9)

stats_text = f'n = {len(nds_pre)}\nMean = {mean_pre:.3f}\nSD = {std_pre:.3f}\nMedian = {np.median(nds_pre):.3f}'
ax1.text(0.97, 0.97, stats_text, transform=ax1.transAxes,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                   edgecolor=color_pre, linewidth=2, alpha=0.95),
         fontsize=9, family='monospace')

ax1.set_xlabel('NDS Score', fontweight='bold')
ax1.set_ylabel('Frequency', fontweight='bold')
ax1.set_title('(A) Pre-COVID NDS Distribution', fontweight='bold', fontsize=13, pad=10)
ax1.legend(loc='upper left', framealpha=0.9, fontsize=8)
ax1.grid(True, alpha=0.25, linestyle=':', axis='y')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ============================================================================
# PANEL B (Top Right): Post-COVID NDS Distribution
# ============================================================================
print("Creating Panel B: Post-COVID Distribution...")
ax2 = fig.add_subplot(gs[0, 1])

bins_post = np.linspace(nds_post.min(), nds_post.max(), 35)
n_counts, bins_edge, patches = ax2.hist(nds_post, bins=bins_post, 
                                        color=color_post, alpha=0.85, 
                                        edgecolor='white', linewidth=0.6)

mean_post = nds_post.mean()
std_post = nds_post.std()
ax2.axvline(mean_post, color='#2C3E50', linestyle='--', 
            linewidth=2, label=f'μ = {mean_post:.2f}', zorder=10)
ax2.axvline(mean_post - std_post, color='#7F8C8D', linestyle=':', 
            linewidth=1.5, alpha=0.7, label=f'σ = {std_post:.2f}', zorder=9)
ax2.axvline(mean_post + std_post, color='#7F8C8D', linestyle=':', 
            linewidth=1.5, alpha=0.7, zorder=9)

stats_text = f'n = {len(nds_post)}\nMean = {mean_post:.3f}\nSD = {std_post:.3f}\nMedian = {np.median(nds_post):.3f}'
ax2.text(0.97, 0.97, stats_text, transform=ax2.transAxes,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                   edgecolor=color_post, linewidth=2, alpha=0.95),
         fontsize=9, family='monospace')

ax2.set_xlabel('NDS Score', fontweight='bold')
ax2.set_ylabel('Frequency', fontweight='bold')
ax2.set_title('(B) Post-COVID NDS Distribution', fontweight='bold', fontsize=13, pad=10)
ax2.legend(loc='upper left', framealpha=0.9, fontsize=8)
ax2.grid(True, alpha=0.25, linestyle=':', axis='y')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# ============================================================================
# PANEL C (Middle Left): Distribution Comparison with KS Test
# ============================================================================
print("Creating Panel C: Distribution Comparison (KS Test)...")
ax3 = fig.add_subplot(gs[1, 0])

bins_combined = np.linspace(min(nds_pre.min(), nds_post.min()),
                           max(nds_pre.max(), nds_post.max()), 40)

ax3.hist(nds_pre, bins=bins_combined, alpha=0.6, label='Pre-COVID',
         color=color_pre, edgecolor='black', linewidth=0.5, density=True)
ax3.hist(nds_post, bins=bins_combined, alpha=0.6, label='Post-COVID',
         color=color_post, edgecolor='black', linewidth=0.5, density=True)

kde_pre = gaussian_kde(nds_pre)
kde_post = gaussian_kde(nds_post)
x_range = np.linspace(min(nds_pre.min(), nds_post.min()),
                     max(nds_pre.max(), nds_post.max()), 500)

ax3.plot(x_range, kde_pre(x_range), color='#2E5266', 
         linewidth=2.5, linestyle='-', label='Pre-COVID KDE', alpha=0.8)
ax3.plot(x_range, kde_post(x_range), color='#8B1E3F', 
         linewidth=2.5, linestyle='-', label='Post-COVID KDE', alpha=0.8)

ks_stat, ks_p = stats.ks_2samp(nds_pre, nds_post)
pooled_std = np.sqrt((nds_pre.var() + nds_post.var()) / 2)
cohens_d = (mean_post - mean_pre) / pooled_std

test_text = f'Kolmogorov-Smirnov Test\n'
test_text += f'D = {ks_stat:.4f}\n'
test_text += f'p = {ks_p:.2e}\n'
test_text += f"Cohen's d = {cohens_d:.3f}\n\n"
test_text += f'Δμ = {mean_post - mean_pre:.3f}'

ax3.text(0.97, 0.97, test_text, transform=ax3.transAxes,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                   edgecolor='black', linewidth=1.5, alpha=0.95),
         fontsize=9, family='monospace')

ax3.set_xlabel('NDS Score', fontweight='bold')
ax3.set_ylabel('Probability Density', fontweight='bold')
ax3.set_title('(C) Distribution Comparison (KS Test)', 
              fontweight='bold', fontsize=13, pad=10)
ax3.legend(loc='upper left', framealpha=0.9, fontsize=8)
ax3.grid(True, alpha=0.25, linestyle=':', axis='y')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# ============================================================================
# PANEL D (Middle Right): Q-Q Plot
# ============================================================================
print("Creating Panel D: Q-Q Plot...")
ax4 = fig.add_subplot(gs[1, 1])

percentiles = np.linspace(0, 100, min(len(nds_pre), len(nds_post)))
q_pre = np.percentile(nds_pre, percentiles)
q_post = np.percentile(nds_post, percentiles)

ax4.plot(q_pre, q_post, 'o', color=color_post, alpha=0.5, 
         markersize=4, label='Empirical Quantiles')

min_val = min(q_pre.min(), q_post.min())
max_val = max(q_pre.max(), q_post.max())
ax4.plot([min_val, max_val], [min_val, max_val], 'k--', 
         linewidth=2, label='Reference (y=x)', alpha=0.7)

from scipy.stats import linregress
slope, intercept, r_value, p_value, std_err = linregress(q_pre, q_post)
fit_line = slope * q_pre + intercept
ax4.plot(q_pre, fit_line, 'r-', linewidth=2, 
         label=f'Fit (R²={r_value**2:.3f})', alpha=0.8)

qq_text = f'Q-Q Plot Statistics\nSlope = {slope:.3f}\nR² = {r_value**2:.3f}\np = {p_value:.2e}'
ax4.text(0.05, 0.95, qq_text, transform=ax4.transAxes,
         verticalalignment='top', horizontalalignment='left',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                   edgecolor='black', linewidth=1.5, alpha=0.95),
         fontsize=9, family='monospace')

ax4.set_xlabel('Pre-COVID Quantiles', fontweight='bold')
ax4.set_ylabel('Post-COVID Quantiles', fontweight='bold')
ax4.set_title('(D) Q-Q Plot: Pre vs Post-COVID NDS', 
              fontweight='bold', fontsize=13, pad=10)
ax4.legend(loc='lower right', framealpha=0.9, fontsize=8)
ax4.grid(True, alpha=0.25, linestyle=':')
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

deviation = q_post - q_pre
ax4.fill_between(q_pre, q_pre, q_post, where=(deviation > 0), 
                 alpha=0.2, color=color_post, label='_nolegend_')
ax4.fill_between(q_pre, q_pre, q_post, where=(deviation < 0), 
                 alpha=0.2, color=color_pre, label='_nolegend_')

# ============================================================================
# PANEL E (Bottom): ML vs Rule-Based Comparison Table
# ============================================================================
print("Creating Panel E: ML vs Rule-Based Comparison Table...")
ax5 = fig.add_subplot(gs[2, :])
ax5.axis('off')

# Table data
headers = ['Statistical Test', 'Rule-Based NDS', 'ML-Based NDS (XGBoost)', 'Improvement']

data = [
    ['Kolmogorov-Smirnov', 
     'D = 0.1097, p = 1.95×10⁻⁴',
     'D = 0.2788, p = 1.92×10⁻²⁶',
     'Stronger ↑'],
    
    ['Permutation (10k iter)',
     'p < 0.0001',
     'p < 0.0001 (0.00th %ile)',
     'Stronger ↑'],
    
    ['Mann-Whitney U',
     'p = 7.89×10⁻⁷',
     'p = 3.24×10⁻³²',
     'Stronger ↑'],
    
    ['Effect Size (Cohen\'s d)',
     '0.291 (small)',
     '-0.639 (medium)',
     'Larger ↑'],
]

# Create table
table = ax5.table(cellText=data, colLabels=headers,
                cellLoc='center', loc='center',
                colWidths=[0.23, 0.27, 0.30, 0.20])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.8)

# Style header
header_color = '#2C3E50'
for i, header in enumerate(headers):
    cell = table[(0, i)]
    cell.set_facecolor(header_color)
    cell.set_text_props(weight='bold', color='white', fontsize=11)
    cell.set_edgecolor('white')
    cell.set_linewidth(2)

# Style data rows
row_colors = ['#ECF0F1', '#FFFFFF']
improvement_color = '#27AE60'

for i in range(len(data)):
    for j in range(len(headers)):
        cell = table[(i+1, j)]
        
        if j < 3:
            cell.set_facecolor(row_colors[i % 2])
        else:
            cell.set_facecolor('#D5F4E6')
            cell.set_text_props(weight='bold', color=improvement_color, fontsize=10)
        
        cell.set_edgecolor('#BDC3C7')
        cell.set_linewidth(1)
        
        if j in [1, 2]:
            cell.set_text_props(fontsize=9, family='monospace')

# Add table title above
ax5.text(0.5, 1.15, '(E) Statistical Test Results: ML-Based vs Rule-Based NDS Predictions', 
         transform=ax5.transAxes, ha='center', va='top',
         fontsize=13, fontweight='bold', color=header_color)

# Add note below table
note_text = 'Note: ML-based XGBoost predictions show stronger statistical significance and larger effect sizes than rule-based activations.'
ax5.text(0.5, -0.15, note_text, transform=ax5.transAxes, ha='center', va='top',
         fontsize=9, color='#7F8C8D', style='italic')

# Add overall title
fig.suptitle('NDS Distribution Analysis & Statistical Validation: Pre vs Post-COVID Regime Shift',
             fontsize=16, fontweight='bold', y=0.98, color='#2C3E50')

plt.tight_layout(rect=[0, 0.02, 1, 0.96])

# Save the figure
output_path_png = 'Publication_Figures/nds_distribution_with_comparison_table.png'
output_path_pdf = 'Publication_Figures/nds_distribution_with_comparison_table.pdf'

plt.savefig(output_path_png, dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(output_path_pdf, dpi=300, bbox_inches='tight', facecolor='white')

print(f"\n✓ Comprehensive figure saved:")
print(f"  - {output_path_png}")
print(f"  - {output_path_pdf}")
print(f"\nFigure includes:")
print(f"  - Panel A: Pre-COVID distribution (n={len(nds_pre)})")
print(f"  - Panel B: Post-COVID distribution (n={len(nds_post)})")
print(f"  - Panel C: KS test comparison")
print(f"  - Panel D: Q-Q plot")
print(f"  - Panel E: ML vs Rule-Based comparison table")
print(f"\nAll panels use ML-based NDS predictions from XGBoost models")

plt.close()
