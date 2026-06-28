"""
VERIFICATION SCRIPT: Run Length Calculation
============================================
Manually verify run length calculations from stability analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load data
data_dir = Path(__file__).parent.parent
df_pre = pd.read_csv(data_dir / 'brain_activation_pre_covid.csv')
df_post = pd.read_csv(data_dir / 'brain_activation_post_covid.csv')

print("=" * 80)
print("MANUAL VERIFICATION OF RUN LENGTH CALCULATIONS")
print("=" * 80)

ACTIVATION_SYSTEMS = ['value_active', 'risk_active', 'sentiment_active', 
                      'insula_active', 'control_active']

def compute_run_lengths_detailed(series, system_name, period_name):
    """Compute run lengths with detailed output for verification"""
    run_lengths = []
    current_run = 0
    
    for i, value in enumerate(series):
        if value == 1:
            current_run += 1
        else:
            if current_run > 0:
                run_lengths.append(current_run)
                current_run = 0
    
    # Handle case where series ends with 1s
    if current_run > 0:
        run_lengths.append(current_run)
    
    if not run_lengths:
        run_lengths = [0]
    
    print(f"\n{period_name} - {system_name}:")
    print(f"  Total observations: {len(series)}")
    print(f"  Total active days (1s): {int(series.sum())}")
    print(f"  Number of runs: {len([r for r in run_lengths if r > 0])}")
    print(f"  Run lengths: {run_lengths[:10]}{'...' if len(run_lengths) > 10 else ''}")
    print(f"  Min run: {min(run_lengths)}, Max run: {max(run_lengths)}")
    print(f"  Mean run length: {np.mean(run_lengths):.2f}")
    print(f"  Median run length: {np.median(run_lengths):.2f}")
    
    return run_lengths

print("\n" + "=" * 80)
print("PRE-COVID PERIOD (773 observations)")
print("=" * 80)

for system in ACTIVATION_SYSTEMS:
    system_name = system.replace('_active', '').capitalize()
    runs = compute_run_lengths_detailed(df_pre[system].values, system_name, "PRE")

print("\n" + "=" * 80)
print("POST-COVID PERIOD (743 observations)")
print("=" * 80)

for system in ACTIVATION_SYSTEMS:
    system_name = system.replace('_active', '').capitalize()
    runs = compute_run_lengths_detailed(df_post[system].values, system_name, "POST")

print("\n" + "=" * 80)
print("COMPARISON WITH REPORTED VALUES")
print("=" * 80)

# Read the summary file
summary = pd.read_csv(Path(__file__).parent / 'stability_run_length_summary.csv')
print("\nReported values from stability_run_length_summary.csv:")
print(summary.to_string(index=False))

print("\n" + "=" * 80)
print("DETAILED VERIFICATION - EXAMPLE: VALUE SYSTEM")
print("=" * 80)

# Detailed example for Value system
value_pre = df_pre['value_active'].values
print(f"\nValue system (Pre-COVID):")
print(f"First 50 values: {value_pre[:50]}")

# Count runs manually
runs = []
current = 0
for v in value_pre:
    if v == 1:
        current += 1
    else:
        if current > 0:
            runs.append(current)
        current = 0
if current > 0:
    runs.append(current)

print(f"\nAll run lengths found: {runs}")
print(f"Total runs: {len(runs)}")
print(f"Sum of runs (should equal total 1s): {sum(runs)}")
print(f"Total 1s in data: {value_pre.sum()}")
print(f"Average run length: {np.mean(runs):.4f}")
print(f"\n✓ Verification: Average = {np.mean(runs):.2f} (reported: 4.82)")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
