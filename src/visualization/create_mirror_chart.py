"""
Mirror Chart for Stability Analysis
Creates a butterfly/mirror chart showing Pre vs Post COVID stability comparison
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("white")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 24

# Load data
OUTPUT_DIR = Path(__file__).parent
run_length_df = pd.read_csv(OUTPUT_DIR / 'stability_run_length_summary.csv')
run_length_df['System'] = run_length_df['System'].replace('Insula', 'Anomaly Detection')

print("="*60)
print("CREATING MIRROR CHART")
print("="*60)

# ============================================================================
# MIRROR CHART: PRE vs POST COVID RUN LENGTHS
# ============================================================================

fig, ax = plt.subplots(figsize=(22, 12))

# Prepare data
systems = run_length_df['System'].values
pre_values = run_length_df['Avg_Run_Length_Pre'].values
post_values = run_length_df['Avg_Run_Length_Post'].values
y_pos = np.arange(len(systems))

# Colors
color_pre = '#3498db'   # Blue for Pre-COVID
color_post = '#e74c3c'  # Red for Post-COVID

# Create horizontal bars (mirror effect)
# Pre-COVID on the left (negative values for visualization)
bars_pre = ax.barh(y_pos, -pre_values, height=0.7, 
                   label='Pre-COVID', color=color_pre, 
                   alpha=0.85, edgecolor='black', linewidth=1.5)

# Post-COVID on the right (positive values)
bars_post = ax.barh(y_pos, post_values, height=0.7, 
                    label='Post-COVID', color=color_post, 
                    alpha=0.85, edgecolor='black', linewidth=1.5)

# Add value labels – outside bar if bar is short, inside if wide
THRESH = 4.0
for i, (pre, post) in enumerate(zip(pre_values, post_values)):
    # Pre-COVID labels (left side)
    if pre < THRESH:
        ax.text(-pre - 0.4, i, f'{pre:.1f}',
                ha='right', va='center', fontsize=36,
                fontweight='bold', color='#1a5276')
    else:
        ax.text(-pre/2, i, f'{pre:.1f}',
                ha='center', va='center', fontsize=36,
                fontweight='bold', color='white')

    # Post-COVID labels (right side)
    if post < THRESH:
        ax.text(post + 0.4, i, f'{post:.1f}',
                ha='left', va='center', fontsize=36,
                fontweight='bold', color='#922b21')
    else:
        ax.text(post/2, i, f'{post:.1f}',
                ha='center', va='center', fontsize=36,
                fontweight='bold', color='white')

# Add percentage change badges near system names (fixed x position at left edge)
max_val = max(pre_values.max(), post_values.max()) + 5
for i, row in run_length_df.iterrows():
    pct_change = row['Pct_Change']
    arrow_color = '#2ecc71' if pct_change > 0 else '#e74c3c'
    
    ax.text(-max_val + 1.5, i, f'+{pct_change}%', 
            ha='left', va='center', fontsize=32, 
            fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.4', 
                     facecolor=arrow_color, alpha=0.9,
                     edgecolor='black', linewidth=1.5))

# Formatting
ax.set_yticks(y_pos)
ax.set_yticklabels(systems, fontsize=36, fontweight='bold')
ax.set_xlabel('Average Run Length (days)', fontsize=38, fontweight='bold')
ax.set_title('System Stability Mirror Chart: Pre vs Post COVID\nRun Length Comparison (days systems stay activated)', 
             fontsize=40, fontweight='bold', pad=20)

# Set x-axis limits and labels
max_val = max(pre_values.max(), post_values.max()) + 5
ax.set_xlim(-max_val, max_val)

# Custom x-axis labels (show absolute values)
x_ticks = np.arange(-35, 40, 5)
x_labels = [str(abs(int(x))) for x in x_ticks]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, fontsize=32)

# Add vertical line at center
ax.axvline(x=0, color='black', linestyle='-', linewidth=2.5, alpha=0.8)

# Add period labels
# Period labels removed – shown in legend instead

# Grid
ax.grid(True, alpha=0.3, axis='x', linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)
ax.set_facecolor('#f8f9fa')

# Legend
ax.legend(loc='lower right', fontsize=38, framealpha=0.95, 
          edgecolor='black', fancybox=True, shadow=True,
          borderpad=1.2, handlelength=2.5, handletextpad=1.0, markerscale=2)

# Add interpretation text
interpretation = "← Pre-COVID Stability  |  Post-COVID Stability →\n(Longer bars = More stable systems)"
plt.tight_layout(rect=[0, 0.10, 1, 1])
fig.text(0.5, 0.03, interpretation, ha='center', fontsize=36, 
         fontweight='bold', style='italic', color='#555555',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.4))

output_file = OUTPUT_DIR / 'stability_mirror_chart.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file.name}")
print("\nMirror Chart Features:")
print("- Butterfly/mirror visualization showing Pre vs Post comparison")
print("- Percentage change displayed in center for each system")
print("- Sentiment shows dramatic difference (20.1 vs 30.6 days)")
print("="*60)
plt.close()
