"""
Rolling Correlation Regimes: Market Alignment Over Time
Descriptive visualization of temporal alignment between brain systems and market variables

Creates rolling correlation plots showing alignment/disalignment regimes
without inferring causality or predictive relationships.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from itertools import combinations

# Set style
sns.set_style("white")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Define paths
DATA_PATH = Path(r'c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels\brain_activation_combined_xgboost.csv')
OUTPUT_DIR = Path(r'c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels\Rolling_Correlation_Regimes')

# Load data
print("Loading XGBoost brain activation data (5 systems)...")
df = pd.read_csv(DATA_PATH)
df['Date'] = pd.to_datetime(df['date'])
df = df.sort_values('Date').reset_index(drop=True)

# Rename activation columns to match expected format
df['Value'] = df['value_active']
df['Risk'] = df['risk_active']
df['Sentiment'] = df['sentiment_active']
df['Insula'] = df['insula_active']
df['Control'] = df['control_active']

# Market return is already in the data
df['market_return'] = df['daily_return']

# Calculate NDS (Neural Decision Score) - weighted combination of all 5 systems
df['nds'] = (0.25 * df['Value'] + 0.25 * df['Risk'] + 0.20 * df['Sentiment'] + 0.15 * df['Insula'] + 0.15 * df['Control'])

print(f"Data loaded: {len(df)} days")
print(f"Period: {df['Date'].min()} to {df['Date'].max()}")
print(f"Systems: Value, Risk, Sentiment, Insula, Control")

# Define rolling window
WINDOW = 60  # 60-day rolling correlation

print(f"\nComputing {WINDOW}-day rolling correlations...")

# Systems to analyze (XGBoost has 5 systems including Insula)
systems = ['Value', 'Risk', 'Sentiment', 'Insula', 'Control']

# Function to create rolling correlation regime graph
def create_correlation_regime_graph(series_a, series_b, label_a, label_b, df, output_dir, filename):
    """
    Create rolling correlation regime visualization
    
    Parameters:
    - series_a, series_b: pandas Series to correlate
    - label_a, label_b: names for the series
    - df: dataframe with Date column
    - output_dir: output directory
    - filename: output filename
    """
    # Compute rolling correlation
    rolling_corr = series_a.rolling(window=WINDOW, min_periods=30).corr(series_b)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 7))
    
    dates = df['Date']
    
    # Fill areas
    # Positive correlation = aligned regime (green)
    ax.fill_between(dates, rolling_corr, 0, 
                     where=(rolling_corr >= 0), 
                     color='#27ae60', 
                     alpha=0.6, 
                     label='Aligned Regime (Corr > 0)',
                     interpolate=False)
    
    # Negative correlation = disaligned regime (red)
    ax.fill_between(dates, rolling_corr, 0, 
                     where=(rolling_corr < 0), 
                     color='#e74c3c', 
                     alpha=0.6, 
                     label='Disaligned Regime (Corr < 0)',
                     interpolate=False)
    
    # Plot correlation line
    ax.plot(dates, rolling_corr, color='black', linewidth=1.5, alpha=0.8, zorder=3)
    
    # Zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.9, zorder=4)
    
    # Add COVID period vertical line
    covid_start = df[df['period'] == 'Post-COVID']['Date'].min()
    if pd.notna(covid_start):
        ax.axvline(x=covid_start, color='darkred', linestyle='--', linewidth=2.5, 
                   alpha=0.7, label='COVID Period Start', zorder=5)
        ax.text(covid_start, ax.get_ylim()[1]*0.95, 'COVID', 
                rotation=90, verticalalignment='top', fontsize=11, 
                color='darkred', fontweight='bold')
    
    # Reference lines
    ax.axhline(y=0.5, color='green', linestyle=':', linewidth=0.8, alpha=0.4, label='Strong Positive')
    ax.axhline(y=-0.5, color='red', linestyle=':', linewidth=0.8, alpha=0.4, label='Strong Negative')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=13, fontweight='bold')
    ax.set_ylabel(f'Rolling Correlation ({WINDOW}-Day)', fontsize=13, fontweight='bold')
    ax.set_title(f'Rolling Correlation Regimes: {label_a} vs {label_b}\nMarket Alignment Over Time', 
                 fontsize=16, fontweight='bold', pad=20)
    
    ax.legend(loc='upper left', fontsize=10, framealpha=0.95, edgecolor='black', fancybox=True)
    ax.grid(True, alpha=0.25, linestyle=':', linewidth=0.8, color='gray')
    ax.set_axisbelow(True)
    ax.set_ylim(-1.05, 1.05)
    
    plt.xticks(rotation=45, ha='right')
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    
    # Save
    output_file = output_dir / filename
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  Saved: {filename}")
    plt.close()
    
    # Return correlation statistics
    pre_corr = rolling_corr[df['period'] == 'Pre-COVID'].mean()
    post_corr = rolling_corr[df['period'] == 'Post-COVID'].mean()
    
    return {
        'Pair': f'{label_a} vs {label_b}',
        'Pre_COVID_Corr': round(pre_corr, 3),
        'Post_COVID_Corr': round(post_corr, 3),
        'Change': round(post_corr - pre_corr, 3),
        'Aligned_%': round((rolling_corr > 0).sum() / len(rolling_corr) * 100, 1)
    }

# Generate correlation graphs
print("\n" + "="*60)
print("GENERATING ROLLING CORRELATION REGIME GRAPHS")
print("="*60)

correlation_stats = []

# 1. Each system vs NDS score
print("\n1. Systems vs NDS Score:")
for system in systems:
    stats = create_correlation_regime_graph(
        df[system], df['nds'], 
        system, 'NDS', 
        df, OUTPUT_DIR,
        f'{system.lower()}_vs_nds_correlation.png'
    )
    correlation_stats.append(stats)

# 2. Each system vs Market Return
print("\n2. Systems vs Market Return:")
for system in systems:
    stats = create_correlation_regime_graph(
        df[system], df['market_return'], 
        system, 'Market Return', 
        df, OUTPUT_DIR,
        f'{system.lower()}_vs_return_correlation.png'
    )
    correlation_stats.append(stats)

# 3. Cross-system correlations (key pairs - includes Insula)
print("\n3. Cross-System Correlations:")
key_pairs = [
    ('Value', 'Sentiment'),
    ('Value', 'Control'),
    ('Risk', 'Sentiment'),
    ('Risk', 'Insula'),
    ('Sentiment', 'Insula'),
    ('Sentiment', 'Control')
]

for sys_a, sys_b in key_pairs:
    stats = create_correlation_regime_graph(
        df[sys_a], df[sys_b], 
        sys_a, sys_b, 
        df, OUTPUT_DIR,
        f'{sys_a.lower()}_vs_{sys_b.lower()}_correlation.png'
    )
    correlation_stats.append(stats)

# Create summary statistics
print("\n" + "="*60)
print("CORRELATION REGIME STATISTICS")
print("="*60)

summary_df = pd.DataFrame(correlation_stats)
print("\n", summary_df.to_string(index=False))

# Save summary
summary_file = OUTPUT_DIR / 'correlation_statistics_summary.csv'
summary_df.to_csv(summary_file, index=False)
print(f"\nSaved summary: {summary_file.name}")

# Create combined multi-panel figure (key correlations)
print("\n" + "="*60)
print("GENERATING COMBINED CORRELATION DASHBOARD")
print("="*60)

fig, axes = plt.subplots(3, 2, figsize=(18, 14), sharex=True)
axes = axes.flatten()

plot_configs = [
    ('Value', 'nds', 'Value vs NDS'),
    ('Sentiment', 'nds', 'Sentiment vs NDS'),
    ('Insula', 'nds', 'Insula vs NDS'),
    ('Risk', 'market_return', 'Risk vs Market Return'),
    ('Risk', 'Sentiment', 'Risk vs Sentiment'),
    ('Sentiment', 'Insula', 'Sentiment vs Insula')
]

for idx, (var_a, var_b, title) in enumerate(plot_configs):
    ax = axes[idx]
    
    # Compute rolling correlation
    rolling_corr = df[var_a].rolling(window=WINDOW, min_periods=30).corr(df[var_b])
    dates = df['Date']
    
    # Fill areas
    ax.fill_between(dates, rolling_corr, 0, 
                     where=(rolling_corr >= 0), 
                     color='#27ae60', alpha=0.6, interpolate=False)
    ax.fill_between(dates, rolling_corr, 0, 
                     where=(rolling_corr < 0), 
                     color='#e74c3c', alpha=0.6, interpolate=False)
    
    # Correlation line
    ax.plot(dates, rolling_corr, color='black', linewidth=1.2, alpha=0.8)
    
    # Zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.9)
    
    # COVID marker
    covid_start = df[df['period'] == 'Post-COVID']['Date'].min()
    if pd.notna(covid_start):
        ax.axvline(x=covid_start, color='darkred', linestyle='--', linewidth=1.5, alpha=0.5)
    
    # Formatting
    ax.set_ylabel('Correlation', fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.25, linestyle=':', linewidth=0.6)
    ax.set_ylim(-1.05, 1.05)
    ax.set_facecolor('#f8f9fa')

# X-axis label only on bottom
axes[-2].set_xlabel('Date', fontsize=12, fontweight='bold')
axes[-1].set_xlabel('Date', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')

fig.suptitle(f'Rolling Correlation Regimes Dashboard ({WINDOW}-Day Window)\nMarket Alignment Dynamics: Pre vs Post COVID', 
             fontsize=16, fontweight='bold', y=0.995)

plt.tight_layout()

output_file = OUTPUT_DIR / 'correlation_regimes_dashboard.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"  Saved combined dashboard: {output_file.name}")
plt.close()

print("\n" + "="*60)
print("VISUALIZATION COMPLETE")
print("="*60)
print(f"\nOutput directory: {OUTPUT_DIR}")
print(f"Generated files:")
print(f"  - {len(correlation_stats)} individual correlation regime graphs")
print(f"  - 1 combined dashboard (6-panel)")
print(f"  - 1 summary statistics CSV")
