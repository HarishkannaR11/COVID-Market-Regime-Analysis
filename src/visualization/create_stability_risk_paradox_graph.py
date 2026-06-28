"""
Create visualization showing Post-COVID Stability-Risk Paradox
- Left panel: Increased regime persistence (run lengths)
- Right panel: Risk-dominant decision landscape (NDS shift)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['font.size'] = 24
plt.rcParams['axes.titlesize'] = 30
plt.rcParams['axes.labelsize'] = 28
plt.rcParams['xtick.labelsize'] = 25
plt.rcParams['ytick.labelsize'] = 25
plt.rcParams['legend.fontsize'] = 26

# Data from research results
systems = ['Value', 'Risk', 'Sentiment', 'Anomaly Detection', 'Control']
run_length_pre = [3.2, 3.1, 3.4, 3.3, 3.2]
run_length_post = [3.8, 3.5, 5.2, 4.1, 3.9]
persistence_increase = [18.8, 12.9, 52.7, 24.2, 21.9]

# NDS distribution statistics
nds_mean_pre = 0.000
nds_mean_post = -2.010
nds_std_pre = 2.014
nds_std_post = 4.853

# Create figure with 2 panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 10))
fig.suptitle('Post-COVID Market Paradox: Increased Stability with Risk-Dominant Decision-Making', 
             fontsize=34, fontweight='bold', y=1.02)

# ============================================================
# LEFT PANEL: Regime Persistence Increase (Stability)
# ============================================================

x = np.arange(len(systems))
width = 0.35

bars1 = ax1.bar(x - width/2, run_length_pre, width, label='Pre-COVID', 
                color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.2)
bars2 = ax1.bar(x + width/2, run_length_post, width, label='Post-COVID', 
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.2)

# Add percentage increase annotations
for i, (pre, post, pct) in enumerate(zip(run_length_pre, run_length_post, persistence_increase)):
    ax1.annotate(f'+{pct}%', 
                xy=(i, post + 0.15), 
                ha='center', 
                fontsize=27, 
                fontweight='bold',
                color='darkgreen')

ax1.set_xlabel('Decision System', fontsize=28, fontweight='bold')
ax1.set_ylabel('Average Run Length (days)', fontsize=28, fontweight='bold')
ax1.set_title('Increased Regime Persistence\n(More Stable States)', 
              fontsize=30, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(systems, rotation=0, ha='center', fontsize=26)
leg1 = ax1.legend(loc='upper left', fontsize=26, framealpha=1.0,
           edgecolor='black', fancybox=True, shadow=True,
           borderpad=1.2, handlelength=2.5, handletextpad=1.0, markerscale=1.5)
leg1.get_frame().set_linewidth(2.5)
leg1.get_frame().set_facecolor('#EAF4FB')
ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim(0, 6)

# Add horizontal line at mean
mean_pre_rl = np.mean(run_length_pre)
mean_post_rl = np.mean(run_length_post)
ax1.axhline(mean_pre_rl, color='#3498db', linestyle='--', alpha=0.5, linewidth=1.5)
ax1.axhline(mean_post_rl, color='#e74c3c', linestyle='--', alpha=0.5, linewidth=1.5)

# Add text box with key finding
textstr1 = 'KEY FINDING:\n✓ All systems more persistent\n✓ Sentiment +52.7% (highest)\n✓ Regimes last longer'
props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.3, edgecolor='darkgreen', linewidth=2)
ax1.text(0.98, 0.97, textstr1, transform=ax1.transAxes, fontsize=24,
         verticalalignment='top', horizontalalignment='right', bbox=props)

# ============================================================
# RIGHT PANEL: Risk Dominance (NDS Distribution Shift)
# ============================================================

# Generate NDS distributions for visualization
np.random.seed(42)
nds_pre_samples = np.random.normal(nds_mean_pre, nds_std_pre, 1000)
nds_post_samples = np.random.normal(nds_mean_post, nds_std_post, 1000)

# Plot KDE distributions
from scipy.stats import gaussian_kde

kde_pre = gaussian_kde(nds_pre_samples)
kde_post = gaussian_kde(nds_post_samples)

x_range = np.linspace(-15, 10, 500)
ax2.fill_between(x_range, kde_pre(x_range), alpha=0.4, color='#3498db', label='Pre-COVID')
ax2.fill_between(x_range, kde_post(x_range), alpha=0.4, color='#e74c3c', label='Post-COVID')

ax2.plot(x_range, kde_pre(x_range), color='#3498db', linewidth=2.5)
ax2.plot(x_range, kde_post(x_range), color='#e74c3c', linewidth=2.5)

# Add mean lines
ax2.axvline(nds_mean_pre, color='#3498db', linestyle='--', linewidth=2.5, alpha=0.8)
ax2.axvline(nds_mean_post, color='#e74c3c', linestyle='--', linewidth=2.5, alpha=0.8)

# Annotate means
ax2.annotate(f'Pre Mean: {nds_mean_pre:.2f}', 
            xy=(nds_mean_pre, 0.12), 
            xytext=(2, 0.12),
            arrowprops=dict(arrowstyle='->', color='#3498db', lw=2),
            fontsize=26, fontweight='bold', color='#3498db')

ax2.annotate(f'Post Mean: {nds_mean_post:.2f}', 
            xy=(nds_mean_post, 0.08), 
            xytext=(-8, 0.08),
            arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2),
            fontsize=26, fontweight='bold', color='#e74c3c')

# Shade risk-dominant region
ax2.axvspan(-15, 0, alpha=0.1, color='red', label='Risk-Dominant Zone')
ax2.axvline(0, color='black', linestyle=':', linewidth=2, alpha=0.5)
ax2.text(0.5, 0.11, 'Neutral', rotation=90, va='center', fontsize=24, alpha=0.6)

ax2.set_xlabel('Neuro-Decision Score (NDS)', fontsize=28, fontweight='bold')
ax2.set_ylabel('Density', fontsize=28, fontweight='bold')
ax2.set_title('Risk-Dominant Decision Landscape\n(Negative NDS Shift)', 
              fontsize=30, fontweight='bold', pad=15)
leg2 = ax2.legend(loc='upper right', fontsize=26, framealpha=1.0,
           edgecolor='black', fancybox=True, shadow=True,
           borderpad=1.2, handlelength=2.5, handletextpad=1.0, markerscale=1.5)
leg2.get_frame().set_linewidth(2.5)
leg2.get_frame().set_facecolor('#EAF4FB')
ax2.grid(axis='both', alpha=0.3)
ax2.set_xlim(-15, 10)

# Add text box with key finding
textstr2 = 'KEY FINDING:\n✗ NDS shifted -2.01\n✗ Risk dominates decisions\n✗ Volatility σ: 2.01→4.85\n✗ Heightened uncertainty'
props2 = dict(boxstyle='round', facecolor='lightcoral', alpha=0.3, edgecolor='darkred', linewidth=2)
ax2.text(0.02, 0.97, textstr2, transform=ax2.transAxes, fontsize=24,
         verticalalignment='top', horizontalalignment='left', bbox=props2)

# Add formula reference
formula_text = 'NDS = Value - Risk + Sentiment\n(Negative = Risk Dominance)'
ax2.text(0.98, 0.30, formula_text, transform=ax2.transAxes, fontsize=23,
         verticalalignment='top', horizontalalignment='right', 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ============================================================
# Overall Layout
# ============================================================

plt.tight_layout()

# Save figure
output_path = 'results/stability_risk_paradox.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"\n✓ Stability-Risk Paradox graph saved to: {output_path}")

plt.show()

# ============================================================
# Additional: Create Paradox Summary Table
# ============================================================

print("\n" + "="*70)
print("POST-COVID MARKET PARADOX SUMMARY")
print("="*70)

summary_data = {
    'Dimension': [
        'Regime Persistence',
        'Risk Influence', 
        'Volatility',
        'Sentiment Stability',
        'Statistical Significance'
    ],
    'Pre-COVID': [
        '3.2 days (avg)',
        'Balanced (NDS≈0)',
        'σ = 2.01',
        '3.4 days',
        'Baseline'
    ],
    'Post-COVID': [
        '3.9 days (avg)',
        'Dominant (NDS=-2.01)',
        'σ = 4.85',
        '5.2 days (+52.7%)',
        'p < 10⁻²⁰'
    ],
    'Interpretation': [
        '✓ MORE STABLE (longer runs)',
        '✗ RISK DOMINATES',
        '✗ INCREASED UNCERTAINTY',
        '✓ MOST STABLE SYSTEM',
        '✓ HIGHLY SIGNIFICANT'
    ]
}

summary_df = pd.DataFrame(summary_data)
print("\n" + summary_df.to_string(index=False))

print("\n" + "="*70)
print("KEY INSIGHT:")
print("="*70)
print("Post-COVID markets are PARADOXICAL: decision systems became more")
print("PERSISTENT (stable regimes) while simultaneously becoming more")
print("RISK-DOMINANT (heightened risk-weighting). This suggests markets")
print("stabilized into a 'new normal' characterized by sustained risk-awareness")
print("rather than returning to pre-pandemic equilibrium.")
print("="*70)
