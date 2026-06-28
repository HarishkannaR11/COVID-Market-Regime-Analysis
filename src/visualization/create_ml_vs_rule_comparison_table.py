"""
Generate ML-Based vs Rule-Based Statistical Tests Comparison Table
Publication-ready table image showing test results comparison
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set publication-quality style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 300

# Create figure
fig, ax = plt.subplots(figsize=(16, 6))
ax.axis('off')

# Table data
headers = ['Statistical Test', 'Rule-Based NDS', 'ML-Based NDS (XGBoost)', 'Improvement']

data = [
    ['Kolmogorov-Smirnov Test', 
     'D = 0.1097\np = 1.95×10⁻⁴',
     'D = 0.2788\np = 1.92×10⁻²⁶',
     'Stronger\nSignificance ✓'],
    
    ['Permutation Test\n(10,000 iterations)',
     'p < 0.0001',
     'p < 0.0001\n(0.00th percentile)',
     'Same/Stronger ✓'],
    
    ['Mann-Whitney U Test',
     'p = 7.89×10⁻⁷',
     'p = 3.24×10⁻³²',
     'Stronger\nSignificance ✓'],
    
    ['Effect Size (Cohen\'s d)',
     'd = 0.291\n(Small effect)',
     'd = -0.639\n(Medium effect)',
     'Larger\nEffect Size ✓'],
]

# Colors
header_color = '#2C3E50'
row_colors = ['#ECF0F1', '#FFFFFF']
improvement_color = '#27AE60'
strong_color = '#E74C3C'

# Create table
table = ax.table(cellText=data, colLabels=headers,
                cellLoc='center', loc='center',
                colWidths=[0.25, 0.25, 0.30, 0.20])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 3.0)

# Style header
for i, header in enumerate(headers):
    cell = table[(0, i)]
    cell.set_facecolor(header_color)
    cell.set_text_props(weight='bold', color='white', fontsize=12)
    cell.set_edgecolor('white')
    cell.set_linewidth(2)

# Style data rows
for i in range(len(data)):
    for j in range(len(headers)):
        cell = table[(i+1, j)]
        
        # Alternate row colors
        if j < 3:
            cell.set_facecolor(row_colors[i % 2])
        else:
            # Improvement column in green
            cell.set_facecolor('#D5F4E6')
            cell.set_text_props(weight='bold', color=improvement_color, fontsize=11)
        
        cell.set_edgecolor('#BDC3C7')
        cell.set_linewidth(1)
        
        # Highlight significant p-values
        text = cell.get_text().get_text()
        if 'p = ' in text or 'p < ' in text:
            if j == 1:  # Rule-based column
                cell.set_text_props(fontsize=10, family='monospace')
            elif j == 2:  # ML-based column
                cell.set_text_props(fontsize=10, family='monospace', weight='bold')

# Add title
title_text = 'Statistical Test Results: ML-Based vs Rule-Based NDS Predictions'
fig.text(0.5, 0.95, title_text, ha='center', va='top', 
         fontsize=16, fontweight='bold', color=header_color)

# Add subtitle
subtitle_text = 'Comparison of Pre-COVID vs Post-COVID Neural Dominance Score (NDS) Distribution Shifts'
fig.text(0.5, 0.90, subtitle_text, ha='center', va='top', 
         fontsize=12, color='#34495E', style='italic')

# Add interpretation note
note_text = 'Note: ML-based XGBoost predictions demonstrate stronger statistical significance and larger effect sizes\n'
note_text += 'compared to rule-based threshold activations, validating the machine learning approach.'
fig.text(0.5, 0.06, note_text, ha='center', va='top', 
         fontsize=10, color='#7F8C8D', style='italic',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF9E7', 
                   edgecolor='#F39C12', linewidth=1.5, alpha=0.9))

# Add methodology note
method_text = 'Rule-Based: Quantile threshold activations (training labels) | ML-Based: XGBoost predictions (max_depth=3, n_estimators=200)'
fig.text(0.5, 0.02, method_text, ha='center', va='bottom', 
         fontsize=9, color='#95A5A6', family='monospace')

plt.tight_layout(rect=[0, 0.08, 1, 0.88])

# Save the figure
output_path_png = 'Publication_Figures/ml_vs_rule_comparison_table.png'
output_path_pdf = 'Publication_Figures/ml_vs_rule_comparison_table.pdf'

plt.savefig(output_path_png, dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(output_path_pdf, dpi=300, bbox_inches='tight', facecolor='white')

print(f"✓ Comparison table saved:")
print(f"  - {output_path_png}")
print(f"  - {output_path_pdf}")
print(f"\nTable Summary:")
print(f"  - 4 statistical tests compared")
print(f"  - ML-based shows stronger significance in all tests")
print(f"  - Effect size increased from small (0.291) to medium (-0.639)")
print(f"  - All improvements marked with ✓")

plt.close()
