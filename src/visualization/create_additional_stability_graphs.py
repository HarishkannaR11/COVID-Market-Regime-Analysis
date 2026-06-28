"""
Additional Stability Visualizations
Creates 3 supplementary graphs for mentor presentation:
1. Switching Frequency (inverse of run length)
2. Stability Matrix Heatmap (compact summary)
3. Pre→Post Line Plot (visual trend comparison)
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
print("GENERATING ADDITIONAL STABILITY VISUALIZATIONS")
print("="*60)

# ============================================================================
# GRAPH 1: SWITCHING FREQUENCY
# ============================================================================
print("\n[1] Creating Switching Frequency Graph...")

# Calculate switching frequency (inverse of run length)
run_length_df['Switching_Freq_Pre'] = 1 / run_length_df['Avg_Run_Length_Pre']
run_length_df['Switching_Freq_Post'] = 1 / run_length_df['Avg_Run_Length_Post']

fig, ax = plt.subplots(figsize=(22, 11))

x = np.arange(len(run_length_df))
width = 0.35

bars1 = ax.bar(x - width/2, run_length_df['Switching_Freq_Pre'], width, 
               label='Pre-COVID', color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.2)
bars2 = ax.bar(x + width/2, run_length_df['Switching_Freq_Post'], width, 
               label='Post-COVID', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.2)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=30, fontweight='bold')

ax.set_xlabel('Cognitive System', fontsize=38, fontweight='bold')
ax.set_ylabel('Switching Frequency (switches/day)', fontsize=38, fontweight='bold')
ax.set_title('System Switching Frequency: Pre vs Post COVID\n(Inverse of Run Length)', 
             fontsize=40, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(run_length_df['System'], fontsize=34)
ax.tick_params(axis='y', labelsize=30)
ax.legend(fontsize=38, framealpha=0.95, edgecolor='black', fancybox=True, shadow=True,
          borderpad=1.2, handlelength=2.5, handletextpad=1.0, markerscale=2)
ax.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)
ax.set_facecolor('#f8f9fa')

# Add interpretation text
interpretation = "Lower switching frequency = More stable system (longer persistence)\nHigher switching frequency = More volatile system (frequent ON/OFF)"
plt.tight_layout(rect=[0, 0.10, 1, 1])
fig.text(0.5, 0.03, interpretation, ha='center', fontsize=36, 
         style='italic', color='#555555', bbox=dict(boxstyle='round', 
         facecolor='wheat', alpha=0.3))

output_file = OUTPUT_DIR / 'stability_switching_frequency.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file.name}")
plt.close()

# ============================================================================
# GRAPH 2: STABILITY MATRIX HEATMAP
# ============================================================================
print("\n[2] Creating Stability Matrix Heatmap...")

# Prepare data for heatmap
heatmap_data = run_length_df[['System', 'Avg_Run_Length_Pre', 'Avg_Run_Length_Post', 'Pct_Change']].copy()
heatmap_data = heatmap_data.set_index('System')

# Rename columns for display
heatmap_data.columns = ['Pre-COVID\n(days)', 'Post-COVID\n(days)', 'Change\n(%)']

fig, ax = plt.subplots(figsize=(10, 6))

# Create heatmap with annotations
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn', 
            cbar_kws={'label': 'Run Length (days) / Change (%)'}, 
            linewidths=2, linecolor='white', ax=ax,
            vmin=0, vmax=50, center=15,
            annot_kws={'fontsize': 12, 'fontweight': 'bold'})

ax.set_title('System Stability Matrix: Run Length Metrics\n(Higher values = More stable/persistent)', 
             fontsize=15, fontweight='bold', pad=20)
ax.set_ylabel('Cognitive System', fontsize=13, fontweight='bold')
ax.set_xlabel('')
ax.tick_params(axis='y', rotation=0)

# Add border
for spine in ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(2)

plt.tight_layout()
output_file = OUTPUT_DIR / 'stability_matrix_heatmap.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file.name}")
plt.close()

# ============================================================================
# GRAPH 3: PRE→POST LINE PLOT
# ============================================================================
print("\n[3] Creating Pre→Post Line Plot...")

fig, ax = plt.subplots(figsize=(12, 8))

# Plot lines connecting Pre to Post for each system
colors = {
    'Value': '#3498db',
    'Risk': '#e74c3c',
    'Sentiment': '#2ecc71',
    'Anomaly Detection': '#9b59b6',
    'Control': '#f39c12'
}

for idx, row in run_length_df.iterrows():
    system = row['System']
    pre_val = row['Avg_Run_Length_Pre']
    post_val = row['Avg_Run_Length_Post']
    pct_change = row['Pct_Change']
    
    # Plot line
    ax.plot([0, 1], [pre_val, post_val], marker='o', markersize=12, 
            linewidth=3, label=f"{system} (+{pct_change}%)",
            color=colors[system], alpha=0.8)
    
    # Add value labels
    ax.text(-0.05, pre_val, f'{pre_val:.1f}', ha='right', va='center', 
            fontsize=10, fontweight='bold', color=colors[system])
    ax.text(1.05, post_val, f'{post_val:.1f}', ha='left', va='center', 
            fontsize=10, fontweight='bold', color=colors[system])

# Formatting
ax.set_xlim(-0.2, 1.2)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Pre-COVID', 'Post-COVID'], fontsize=13, fontweight='bold')
ax.set_ylabel('Average Run Length (days)', fontsize=13, fontweight='bold')
ax.set_title('System Stability Trends: Pre vs Post COVID Transition\nSlope indicates magnitude of stability change', 
             fontsize=15, fontweight='bold', pad=20)

# Legend positioned to highlight Sentiment
ax.legend(loc='upper left', fontsize=11, framealpha=0.95, 
          edgecolor='black', fancybox=True, shadow=True,
          title='System (% Change)', title_fontsize=12)

ax.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)
ax.set_facecolor('#f8f9fa')

# Add annotation for Sentiment (largest change)
sentiment_row = run_length_df[run_length_df['System'] == 'Sentiment'].iloc[0]
ax.annotate('Largest Increase\n+52.7%', 
            xy=(0.5, sentiment_row['Avg_Run_Length_Post']),
            xytext=(0.5, sentiment_row['Avg_Run_Length_Post'] + 5),
            ha='center', fontsize=11, fontweight='bold', color='#2ecc71',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', lw=2, color='#2ecc71'))

plt.tight_layout()
output_file = OUTPUT_DIR / 'stability_pre_post_trend.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file.name}")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("VISUALIZATION COMPLETE")
print("="*60)
print("\nGenerated Files:")
print("1. stability_switching_frequency.png - Inverse run length comparison")
print("2. stability_matrix_heatmap.png - Compact summary matrix")
print("3. stability_pre_post_trend.png - Dramatic trend visualization")
print("\nKey Findings:")
print(f"- Lowest switching frequency: Sentiment (Post: {run_length_df[run_length_df['System']=='Sentiment']['Switching_Freq_Post'].values[0]:.3f} switches/day)")
print(f"- Highest switching frequency: Anomaly Detection (Post: {run_length_df[run_length_df['System']=='Anomaly Detection']['Switching_Freq_Post'].values[0]:.3f} switches/day)")
print(f"- Largest stability increase: Sentiment (+52.7%)")
print("="*60)
