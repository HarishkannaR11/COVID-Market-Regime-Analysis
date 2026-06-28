"""
STABILITY ANALYSIS OF COGNITIVE STATES
=======================================
Run Length & Entropy Analysis for Market Decision States

Objective:
    Evaluate stability of market decision states by measuring:
    1. State persistence (Run Length)
    2. Global instability (Activation Entropy)
    
Methodology:
    - Run Length: Average consecutive sequences of activation (1s)
    - Shannon Entropy: H = -Σ p_i log(p_i) where p_i is activation proportion
    
Academic Constraints:
    - NO trading signals
    - NO investor psychology claims
    - NO new feature engineering
    - Conservative, academic language only
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

# Import seaborn carefully to avoid scipy conflicts
try:
    import seaborn as sns
except Exception:
    sns = None  # Will use matplotlib directly if seaborn fails

# ============================================================================
# CONFIGURATION
# ============================================================================

# Data paths - using combined XGBoost dataset
DATA_PATH_COMBINED = Path(__file__).resolve().parents[1] / 'brain_activation_combined_xgboost.csv'
OUTPUT_DIR = Path(__file__).parent

# Activation systems
ACTIVATION_SYSTEMS = ['value_active', 'risk_active', 'sentiment_active', 
                      'insula_active', 'control_active']

print("=" * 80)
print("STABILITY ANALYSIS: RUN LENGTH & ENTROPY")
print("=" * 80)

# ============================================================================
# SECTION 1: DATA LOADING
# ============================================================================

print("\n[1] Loading Data...")

# Load combined XGBoost dataset
df_combined = pd.read_csv(DATA_PATH_COMBINED)
print(f"✓ Loaded Combined XGBoost Data: {len(df_combined)} observations")

# Ensure date column exists and is datetime
if 'date' in df_combined.columns:
    df_combined['Date'] = pd.to_datetime(df_combined['date'])
elif 'Date' not in df_combined.columns:
    raise ValueError("Dataset must contain 'Date' or 'date' column")
else:
    df_combined['Date'] = pd.to_datetime(df_combined['Date'])

# Verify activation columns exist
missing_cols = [col for col in ACTIVATION_SYSTEMS if col not in df_combined.columns]
if missing_cols:
    raise ValueError(f"Missing activation columns: {missing_cols}")

# Verify period column exists
if 'period' not in df_combined.columns:
    raise ValueError("Dataset must contain 'period' column (Pre-COVID/Post-COVID)")

# Sort by date
df_combined = df_combined.sort_values('Date').reset_index(drop=True)

# Split into Pre and Post COVID periods
df_pre = df_combined[df_combined['period'] == 'Pre-COVID'].copy().reset_index(drop=True)
df_post = df_combined[df_combined['period'] == 'Post-COVID'].copy().reset_index(drop=True)

print(f"✓ Split into Pre-COVID: {len(df_pre)} observations")
print(f"✓ Split into Post-COVID: {len(df_post)} observations")

# ============================================================================
# SECTION 2: PERIOD SEGMENTATION
# ============================================================================

print("\n[2] Period Segmentation...")

print(f"Pre-COVID:  {len(df_pre)} observations ({df_pre['Date'].min().date()} to {df_pre['Date'].max().date()})")
print(f"Post-COVID: {len(df_post)} observations ({df_post['Date'].min().date()} to {df_post['Date'].max().date()})")

# ============================================================================
# SECTION 3: RUN LENGTH ANALYSIS
# ============================================================================

print("\n[3] Run Length Analysis...")
print("Calculating consecutive sequences of activation (1s)...")

def compute_run_lengths(series):
    """
    Compute run lengths for consecutive 1s in a binary series.
    
    Parameters:
        series: Binary series (0s and 1s)
        
    Returns:
        List of run lengths (number of consecutive 1s)
    """
    run_lengths = []
    current_run = 0
    
    for value in series:
        if value == 1:
            current_run += 1
        else:
            if current_run > 0:
                run_lengths.append(current_run)
                current_run = 0
    
    # Handle case where series ends with 1s
    if current_run > 0:
        run_lengths.append(current_run)
    
    return run_lengths if run_lengths else [0]  # Return [0] if no runs found


def summarize_run_lengths(df, systems):
    """
    Summarize run length statistics for all activation systems.
    
    Parameters:
        df: DataFrame with activation columns
        systems: List of activation column names
        
    Returns:
        Dictionary with run length statistics
    """
    results = {}
    
    for system in systems:
        run_lengths = compute_run_lengths(df[system].values)
        results[system] = {
            'avg_run_length': np.mean(run_lengths),
            'median_run_length': np.median(run_lengths),
            'max_run_length': np.max(run_lengths),
            'num_runs': len(run_lengths),
            'total_active_days': df[system].sum()
        }
    
    return results


# Compute run lengths for both periods
run_length_pre = summarize_run_lengths(df_pre, ACTIVATION_SYSTEMS)
run_length_post = summarize_run_lengths(df_post, ACTIVATION_SYSTEMS)

# Create comparison table
run_length_comparison = []

for system in ACTIVATION_SYSTEMS:
    system_name = system.replace('_active', '').capitalize()
    
    avg_pre = run_length_pre[system]['avg_run_length']
    avg_post = run_length_post[system]['avg_run_length']
    diff = avg_post - avg_pre
    pct_change = ((avg_post / avg_pre) - 1) * 100 if avg_pre > 0 else 0
    
    run_length_comparison.append({
        'System': system_name,
        'Avg_Run_Length_Pre': round(avg_pre, 2),
        'Avg_Run_Length_Post': round(avg_post, 2),
        'Difference': round(diff, 2),
        'Pct_Change': round(pct_change, 1)
    })

df_run_length = pd.DataFrame(run_length_comparison)

print("\nRun Length Summary:")
print(df_run_length.to_string(index=False))

# ============================================================================
# SECTION 4: ACTIVATION ENTROPY ANALYSIS
# ============================================================================

print("\n[4] Activation Entropy Analysis...")
print("Computing Shannon entropy: H = -Σ p_i log(p_i)...")

def compute_activation_entropy(df, systems):
    """
    Compute Shannon entropy of activation proportions.
    
    H = -Σ p_i log(p_i)
    
    Where p_i is the proportion of time each system is active.
    
    Parameters:
        df: DataFrame with activation columns
        systems: List of activation column names
        
    Returns:
        Entropy value (in bits)
    """
    # Calculate activation proportions
    proportions = []
    for system in systems:
        p = df[system].mean()  # Proportion of 1s
        if p > 0:  # Only include systems with non-zero activation
            proportions.append(p)
    
    # Normalize to sum to 1
    proportions = np.array(proportions)
    proportions = proportions / proportions.sum()
    
    # Calculate Shannon entropy (using log base 2 for bits)
    entropy = -np.sum(proportions * np.log2(proportions))
    
    return entropy, proportions


# Compute entropy for both periods
entropy_pre, proportions_pre = compute_activation_entropy(df_pre, ACTIVATION_SYSTEMS)
entropy_post, proportions_post = compute_activation_entropy(df_post, ACTIVATION_SYSTEMS)

# Create entropy table
entropy_comparison = pd.DataFrame({
    'Period': ['Pre-COVID', 'Post-COVID'],
    'Entropy_Bits': [round(entropy_pre, 3), round(entropy_post, 3)],
    'Difference': [0, round(entropy_post - entropy_pre, 3)],
    'Pct_Change': [0, round(((entropy_post / entropy_pre) - 1) * 100, 1)]
})

print("\nActivation Entropy Summary:")
print(entropy_comparison.to_string(index=False))

# Print activation proportions
print("\nActivation Proportions (Post-Normalization):")
for i, system in enumerate(ACTIVATION_SYSTEMS):
    system_name = system.replace('_active', '').capitalize()
    print(f"  {system_name:12s}: Pre={proportions_pre[i]:.3f}, Post={proportions_post[i]:.3f}")

# ============================================================================
# SECTION 5: STATISTICAL INTERPRETATION
# ============================================================================

print("\n[5] Generating Academic Interpretation...")

interpretation = f"""STABILITY ANALYSIS INTERPRETATION
===================================

Run Length Analysis:

The analysis of state persistence reveals the following temporal patterns. Average run lengths for Pre-COVID versus Post-COVID periods show:

"""

# Add run length findings
for _, row in df_run_length.iterrows():
    if row['Pct_Change'] > 0:
        direction = "increased"
    else:
        direction = "decreased"
    
    interpretation += f"- {row['System']}: {row['Avg_Run_Length_Pre']:.2f} → {row['Avg_Run_Length_Post']:.2f} days ({direction} {abs(row['Pct_Change']):.1f}%)\n"

# Entropy findings
entropy_direction = "increased" if entropy_post > entropy_pre else "decreased"
interpretation += f"""
Activation Entropy:

Shannon entropy of activation proportions {entropy_direction} from {entropy_pre:.3f} bits (Pre-COVID) to {entropy_post:.3f} bits (Post-COVID), representing a change of {abs(entropy_post - entropy_pre):.3f} bits ({abs(entropy_comparison.iloc[1]['Pct_Change']):.1f}%).

"""

# Generate conservative academic statement
if entropy_post > entropy_pre:
    stability_statement = "increased entropy suggests greater diversity in activation patterns"
else:
    stability_statement = "decreased entropy indicates reduced diversity in activation patterns"

if df_run_length['Pct_Change'].mean() > 0:
    persistence_statement = "longer average run lengths indicate increased state persistence"
else:
    persistence_statement = "shorter average run lengths suggest more frequent regime transitions"

interpretation += f"""Academic Summary:

Run length analysis indicates {persistence_statement} in the Post-COVID period. Concurrently, activation entropy analysis reveals {stability_statement}, suggesting structural changes in the temporal dynamics of market decision states. These findings document quantifiable shifts in state persistence and switching behavior following COVID-19, without implying directional predictions or trading signals.

Note: This analysis measures temporal persistence only and does not constitute trading advice or claims about investor psychology.
"""

print(interpretation)

# ============================================================================
# SECTION 6: SAVE RESULTS
# ============================================================================

print("\n[6] Saving Results...")

# Save run length table
run_length_path = OUTPUT_DIR / 'stability_run_length_summary.csv'
df_run_length.to_csv(run_length_path, index=False)
print(f"✓ Saved: {run_length_path.name}")

# Save entropy table
entropy_path = OUTPUT_DIR / 'stability_entropy_summary.csv'
entropy_comparison.to_csv(entropy_path, index=False)
print(f"✓ Saved: {entropy_path.name}")

# Save interpretation
interpretation_path = OUTPUT_DIR / 'stability_interpretation.txt'
with open(interpretation_path, 'w', encoding='utf-8') as f:
    f.write(interpretation)
print(f"✓ Saved: {interpretation_path.name}")

# ============================================================================
# SECTION 7: VISUALIZATION
# ============================================================================

print("\n[7] Creating Visualizations...")

# Set publication style
plt.style.use('seaborn-v0_8-darkgrid')
if sns is not None:
    sns.set_palette("Set2")

# -------------------------------------------------------------------------
# PLOT 1: Run Length Comparison (Bar Chart)
# -------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

x = np.arange(len(df_run_length))
width = 0.35

bars1 = ax.bar(x - width/2, df_run_length['Avg_Run_Length_Pre'], width, 
               label='Pre-COVID', color='steelblue', alpha=0.8)
bars2 = ax.bar(x + width/2, df_run_length['Avg_Run_Length_Post'], width,
               label='Post-COVID', color='coral', alpha=0.8)

ax.set_xlabel('Decision System', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Run Length (Days)', fontsize=12, fontweight='bold')
ax.set_title('State Persistence: Average Run Length by System\n(Pre-COVID vs Post-COVID)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df_run_length['System'], rotation=0)
ax.legend(loc='upper left', fontsize=11)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plot1_path = OUTPUT_DIR / 'stability_run_length_comparison.png'
plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {plot1_path.name}")

# -------------------------------------------------------------------------
# PLOT 2: Entropy Comparison (Bar Chart)
# -------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

periods = entropy_comparison['Period'].tolist()
entropies = entropy_comparison['Entropy_Bits'].tolist()
colors = ['steelblue', 'coral']

bars = ax.bar(periods, entropies, color=colors, alpha=0.8, width=0.5)

ax.set_ylabel('Shannon Entropy (Bits)', fontsize=12, fontweight='bold')
ax.set_title('Activation Entropy: System Diversity\n(Pre-COVID vs Post-COVID)', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add reference line for maximum entropy (log2(5) = 2.322 for 5 systems)
max_entropy = np.log2(len(ACTIVATION_SYSTEMS))
ax.axhline(max_entropy, color='red', linestyle='--', linewidth=1.5, 
           label=f'Max Entropy = {max_entropy:.3f}')
ax.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plot2_path = OUTPUT_DIR / 'stability_entropy_comparison.png'
plt.savefig(plot2_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {plot2_path.name}")

# -------------------------------------------------------------------------
# PLOT 3: Run Length Distribution (Violin Plot)
# -------------------------------------------------------------------------

# Prepare data for violin plot
run_length_data = []

for system in ACTIVATION_SYSTEMS:
    system_name = system.replace('_active', '').capitalize()
    
    # Pre-COVID runs
    runs_pre = compute_run_lengths(df_pre[system].values)
    for run in runs_pre:
        run_length_data.append({
            'System': system_name,
            'Period': 'Pre-COVID',
            'Run_Length': run
        })
    
    # Post-COVID runs
    runs_post = compute_run_lengths(df_post[system].values)
    for run in runs_post:
        run_length_data.append({
            'System': system_name,
            'Period': 'Post-COVID',
            'Run_Length': run
        })

df_run_dist = pd.DataFrame(run_length_data)

fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

# Use seaborn if available, otherwise matplotlib
if sns is not None:
    sns.violinplot(data=df_run_dist, x='System', y='Run_Length', hue='Period',
                   split=True, palette={'Pre-COVID': 'steelblue', 'Post-COVID': 'coral'},
                   alpha=0.7, ax=ax)
else:
    # Fallback to box plots if seaborn not available
    positions_pre = np.arange(len(ACTIVATION_SYSTEMS)) - 0.2
    positions_post = np.arange(len(ACTIVATION_SYSTEMS)) + 0.2
    
    data_pre = [df_run_dist[(df_run_dist['System'] == sys) & (df_run_dist['Period'] == 'Pre-COVID')]['Run_Length'].values
                for sys in [s.replace('_active', '').capitalize() for s in ACTIVATION_SYSTEMS]]
    data_post = [df_run_dist[(df_run_dist['System'] == sys) & (df_run_dist['Period'] == 'Post-COVID')]['Run_Length'].values
                 for sys in [s.replace('_active', '').capitalize() for s in ACTIVATION_SYSTEMS]]
    
    bp1 = ax.boxplot(data_pre, positions=positions_pre, widths=0.3, patch_artist=True,
                     boxprops=dict(facecolor='steelblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2))
    bp2 = ax.boxplot(data_post, positions=positions_post, widths=0.3, patch_artist=True,
                     boxprops=dict(facecolor='coral', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2))
    
    ax.set_xticks(np.arange(len(ACTIVATION_SYSTEMS)))
    ax.set_xticklabels([s.replace('_active', '').capitalize() for s in ACTIVATION_SYSTEMS])
    ax.legend([bp1["boxes"][0], bp2["boxes"][0]], ['Pre-COVID', 'Post-COVID'], 
             title='Period', fontsize=11)

ax.set_xlabel('Decision System', fontsize=12, fontweight='bold')
ax.set_ylabel('Run Length (Days)', fontsize=12, fontweight='bold')
ax.set_title('Run Length Distribution by System\n(Pre-COVID vs Post-COVID)', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')
if sns is not None:
    ax.legend(title='Period', fontsize=11, title_fontsize=12)

plt.tight_layout()
plot3_path = OUTPUT_DIR / 'stability_run_length_distribution.png'
plt.savefig(plot3_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {plot3_path.name}")

# -------------------------------------------------------------------------
# PLOT 4: Activation Proportion Breakdown (Stacked Bar)
# -------------------------------------------------------------------------

# Calculate activation proportions (NOT normalized)
activation_props_pre = {system.replace('_active', '').capitalize(): 
                        df_pre[system].mean() for system in ACTIVATION_SYSTEMS}
activation_props_post = {system.replace('_active', '').capitalize(): 
                         df_post[system].mean() for system in ACTIVATION_SYSTEMS}

systems_names = list(activation_props_pre.keys())
props_pre = list(activation_props_pre.values())
props_post = list(activation_props_post.values())

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

x = np.arange(2)
width = 0.15

for i, system in enumerate(systems_names):
    ax.bar(x, [props_pre[i], props_post[i]], width, 
           label=system, bottom=[sum(props_pre[:i]), sum(props_post[:i])])

ax.set_ylabel('Activation Proportion', fontsize=12, fontweight='bold')
ax.set_title('System Activation Proportions\n(Pre-COVID vs Post-COVID)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(['Pre-COVID', 'Post-COVID'])
ax.legend(title='System', loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plot4_path = OUTPUT_DIR / 'stability_activation_proportions.png'
plt.savefig(plot4_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {plot4_path.name}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print("\nGenerated Files:")
print(f"1. {run_length_path.name}")
print(f"2. {entropy_path.name}")
print(f"3. {interpretation_path.name}")
print(f"4. {plot1_path.name}")
print(f"5. {plot2_path.name}")
print(f"6. {plot3_path.name}")
print(f"7. {plot4_path.name}")
print("\nKey Findings:")
print(f"- Average Run Length Change: {df_run_length['Pct_Change'].mean():.1f}%")
print(f"- Entropy Change: {entropy_comparison.iloc[1]['Difference']:.3f} bits ({entropy_comparison.iloc[1]['Pct_Change']:.1f}%)")
print("\n" + "=" * 80)
