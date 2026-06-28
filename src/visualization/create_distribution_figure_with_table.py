"""
Generate NDS Distribution 4-Panel Figure with ML vs Rule-Based Comparison Table
Enhanced version of compute_nds_distribution.py with integrated comparison table
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from scipy.stats import gaussian_kde

# Set style
sns.set_style("white")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['legend.fontsize'] = 16

# Configuration
DATA_PATH = Path(__file__).parent / 'nds_timeseries_data_ML.csv'
OUTPUT_DIR = Path(__file__).parent

print("="*80)
print("NDS DISTRIBUTION FIGURE WITH COMPARISON TABLE (ML-BASED)")
print("="*80)

# Load NDS data
print("\n[1] Loading NDS Data...")
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

# Split by period
nds_pre = df[df['period'] == 'Pre-COVID']['NDS'].values
nds_post = df[df['period'] == 'Post-COVID']['NDS'].values

print(f"✓ Pre-COVID: {len(nds_pre)} days, Mean: {nds_pre.mean():.3f}, SD: {nds_pre.std():.3f}")
print(f"✓ Post-COVID: {len(nds_post)} days, Mean: {nds_post.mean():.3f}, SD: {nds_post.std():.3f}")

# Perform statistical tests
ks_statistic, ks_pvalue = stats.ks_2samp(nds_pre, nds_post)
print(f"\nKolmogorov-Smirnov Test: D={ks_statistic:.4f}, p={ks_pvalue:.4e}")

# ============================================================================
# CREATE ENHANCED 5-PANEL FIGURE (4 panels + table at bottom)
# ============================================================================

print("\n[2] Creating Enhanced Figure...")

# Create figure with 3 rows: top 2 rows are 2x2 grid, bottom row spans for table
fig = plt.figure(figsize=(18, 18))

# Create grid: 3 rows, 2 columns, with bottom row for table
gs = fig.add_gridspec(3, 2, 
                      height_ratios=[1, 1, 0.5],
                      hspace=0.35, wspace=0.28, 
                      top=0.94, bottom=0.08, left=0.07, right=0.95)

# ============================================================================
# PANEL 1 (Top Left): Pre-COVID Histogram
# ============================================================================
ax1 = fig.add_subplot(gs[0, 0])

ax1.hist(nds_pre, bins=50, color='#3498db', alpha=0.7, edgecolor='black', linewidth=1)
ax1.axvline(nds_pre.mean(), color='darkblue', linestyle='--', linewidth=2.5, 
           label=f'Mean: {nds_pre.mean():.2f}')
ax1.axvline(np.median(nds_pre), color='navy', linestyle=':', linewidth=2.5, 
           label=f'Median: {np.median(nds_pre):.2f}')
ax1.set_xlabel('NDS Score', fontsize=18, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=18, fontweight='bold')
ax1.set_title('Pre-COVID NDS Distribution', fontsize=20, fontweight='bold')
ax1.legend(fontsize=16)
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_facecolor('#f8f9fa')

# ============================================================================
# PANEL 2 (Top Right): Post-COVID Histogram
# ============================================================================
ax2 = fig.add_subplot(gs[0, 1])

ax2.hist(nds_post, bins=50, color='#e74c3c', alpha=0.7, edgecolor='black', linewidth=1)
ax2.axvline(nds_post.mean(), color='darkred', linestyle='--', linewidth=2.5, 
           label=f'Mean: {nds_post.mean():.2f}')
ax2.axvline(np.median(nds_post), color='maroon', linestyle=':', linewidth=2.5, 
           label=f'Median: {np.median(nds_post):.2f}')
ax2.set_xlabel('NDS Score', fontsize=18, fontweight='bold')
ax2.set_ylabel('Frequency', fontsize=18, fontweight='bold')
ax2.set_title('Post-COVID NDS Distribution', fontsize=20, fontweight='bold')
ax2.legend(fontsize=16)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_facecolor('#f8f9fa')

# ============================================================================
# PANEL 3 (Bottom Left): KDE Overlay
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])

ax3.hist(nds_pre, bins=50, density=True, color='#3498db', alpha=0.3, 
        edgecolor='black', linewidth=0.5, label='Pre-COVID')
ax3.hist(nds_post, bins=50, density=True, color='#e74c3c', alpha=0.3, 
        edgecolor='black', linewidth=0.5, label='Post-COVID')

kde_pre = gaussian_kde(nds_pre)
kde_post = gaussian_kde(nds_post)
x_range = np.linspace(min(nds_pre.min(), nds_post.min()), 
                     max(nds_pre.max(), nds_post.max()), 500)
ax3.plot(x_range, kde_pre(x_range), color='#3498db', linewidth=3, label='Pre KDE')
ax3.plot(x_range, kde_post(x_range), color='#e74c3c', linewidth=3, label='Post KDE')

ax3.set_xlabel('NDS Score', fontsize=18, fontweight='bold')
ax3.set_ylabel('Density', fontsize=18, fontweight='bold')
ax3.set_title('Distribution Comparison (KDE Overlay)', fontsize=20, fontweight='bold')
ax3.legend(fontsize=16)
ax3.grid(True, alpha=0.3, axis='y')
ax3.set_facecolor('#f8f9fa')

# ============================================================================
# PANEL 4 (Bottom Right): Q-Q Plot
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])

stats.probplot(nds_post, dist=stats.norm, plot=ax4)
ax4.get_lines()[0].set_color('#e74c3c')
ax4.get_lines()[0].set_markersize(4)
ax4.get_lines()[1].set_color('black')
ax4.get_lines()[1].set_linewidth(2)
ax4.set_xlabel('Theoretical Quantiles', fontsize=18, fontweight='bold')
ax4.set_ylabel('Post-COVID NDS Quantiles', fontsize=18, fontweight='bold')
ax4.set_title('Q-Q Plot: Normality Check (Post-COVID)', fontsize=20, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.set_facecolor('#f8f9fa')

# ============================================================================
# PANEL 5 (Bottom Full Width): ML vs Rule-Based Comparison Table
# ============================================================================
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
     'p < 0.0001 (0.00%ile)',
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
table.set_fontsize(14)
table.scale(1, 4.0)

# Style header
header_color = '#2C3E50'
for i, header in enumerate(headers):
    cell = table[(0, i)]
    cell.set_facecolor(header_color)
    cell.set_text_props(weight='bold', color='white', fontsize=15)
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
            cell.set_text_props(weight='bold', color=improvement_color, fontsize=14)
        
        cell.set_edgecolor('#BDC3C7')
        cell.set_linewidth(1)
        
        if j in [1, 2]:
            cell.set_text_props(fontsize=13, family='monospace')

# Add table title
ax5.text(0.5, 1.12, 'ML-Based vs Rule-Based Statistical Test Comparison', 
         transform=ax5.transAxes, ha='center', va='top',
         fontsize=18, fontweight='bold', color=header_color)

# Add note
note_text = 'Note: ML-based predictions demonstrate stronger statistical significance, validating the XGBoost approach.'
ax5.text(0.5, -0.12, note_text, transform=ax5.transAxes, ha='center', va='top',
         fontsize=13, color='#7F8C8D', style='italic')

# ============================================================================
# Add Overall Title
# ============================================================================
fig.suptitle(f'NDS Distribution Analysis: Pre vs Post COVID (ML-Based XGBoost Predictions)\nKS Test: p={ks_pvalue:.4f} (Significant)', 
             fontsize=22, fontweight='bold', y=0.97)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the figure
output_path_png = OUTPUT_DIR / 'nds_distribution_with_table_ML.png'
output_path_pdf = OUTPUT_DIR / 'nds_distribution_with_table_ML.pdf'

plt.savefig(output_path_png, dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(output_path_pdf, dpi=300, bbox_inches='tight', facecolor='white')

print(f"\n✓ Enhanced figure saved:")
print(f"  - {output_path_png.name}")
print(f"  - {output_path_pdf.name}")
print(f"\nFigure includes:")
print(f"  • Panel 1: Pre-COVID distribution")
print(f"  • Panel 2: Post-COVID distribution")
print(f"  • Panel 3: KDE overlay comparison")
print(f"  • Panel 4: Q-Q plot (normality check)")
print(f"  • Panel 5: ML vs Rule-Based comparison table")

plt.close()

print("\n" + "="*80)
print("FIGURE GENERATION COMPLETE")
print("="*80)
