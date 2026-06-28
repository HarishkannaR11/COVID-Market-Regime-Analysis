"""
Quick visualization generator for NDS analysis
Regenerates any missing plots from saved CSV files
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

print("Loading NDS data...")
df = pd.read_csv('Results_NDS_Stability/nds_timeseries.csv')
df['Date'] = pd.to_datetime(df['Date'])

df_pre = df[df['Period'] == 'Pre-COVID']
df_post = df[df['Period'] == 'Post-COVID']

summary = pd.read_csv('Results_NDS_Stability/nds_stability_summary.csv')

print("Generating missing visualizations...")

# Extract values from summary
rational_pre = float(summary[summary['Metric'] == 'Rational Regime (%)']['Pre_COVID'].values[0])
rational_post = float(summary[summary['Metric'] == 'Rational Regime (%)']['Post_COVID'].values[0])
fear_pre = float(summary[summary['Metric'] == 'Fear-Dominant Regime (%)']['Pre_COVID'].values[0])
fear_post = float(summary[summary['Metric'] == 'Fear-Dominant Regime (%)']['Post_COVID'].values[0])
mixed_pre = float(summary[summary['Metric'] == 'Mixed Regime (%)']['Pre_COVID'].values[0])
mixed_post = float(summary[summary['Metric'] == 'Mixed Regime (%)']['Post_COVID'].values[0])

# Plot: NDS Regime Frequencies
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

regimes = ['Rational', 'Mixed/Conflicted', 'Fear-Dominant']
pre_vals = [rational_pre, mixed_pre, fear_pre]
post_vals = [rational_post, mixed_post, fear_post]

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

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('Results_NDS_Stability/nds_regimes.png', dpi=300, bbox_inches='tight')
print("✓ Saved: nds_regimes.png")
plt.close()

# Plot: Run Length Comparison
system_names = ['Value', 'Risk', 'Sentiment', 'Insula', 'Control']
pre_runs = []
post_runs = []

for system in system_names:
    metric_name = f'{system} Run Length (days)'
    pre_val = float(summary[summary['Metric'] == metric_name]['Pre_COVID'].values[0])
    post_val = float(summary[summary['Metric'] == metric_name]['Post_COVID'].values[0])
    pre_runs.append(pre_val)
    post_runs.append(post_val)

fig, ax = plt.subplots(1, 1, figsize=(12, 7))

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

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('Results_NDS_Stability/run_length_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: run_length_comparison.png")
plt.close()

print("\n✅ All visualizations complete!")
