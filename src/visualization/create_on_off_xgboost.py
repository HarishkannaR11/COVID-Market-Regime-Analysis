"""
ON vs OFF Time-Series Regime Visualization - XGBoost Data (5 Systems)
Creates Risk-On/Risk-Off style graphs for all cognitive systems including Insula

Uses finalized XGBoost analysis data for research paper
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("white")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['font.family'] = 'sans-serif'

# Define paths
DATA_PATH = Path(r'c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels\brain_activation_combined_xgboost.csv')
OUTPUT_DIR = Path(r'c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels\ON_OFF_Regime_Graphs')

# Load data
print("Loading XGBoost brain activation data (5 systems)...")
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

print(f"Data loaded: {len(df)} days, Period: {df['date'].min()} to {df['date'].max()}")

# Define systems (XGBoost has 5 systems)
systems = ['value', 'risk', 'sentiment', 'insula', 'control']
system_labels = {
    'value': 'Value',
    'risk': 'Risk',
    'sentiment': 'Sentiment',
    'insula': 'Insula',
    'control': 'Control'
}

rolling_window = 30  # 30-day rolling window

def create_on_off_signal(series, window=30):
    """Create ON/OFF signal with rolling window smoothing"""
    median = series.median()
    binary = np.where(series > median, 1, -1)
    smoothed = pd.Series(binary).rolling(window=window, min_periods=1, center=False).mean()
    return smoothed

# Process each system
print(f"\nCreating ON/OFF signals with {rolling_window}-day rolling window...")

for system in systems:
    activation_col = f'{system}_active'
    df[f'{system}_ON_OFF'] = create_on_off_signal(df[activation_col], window=rolling_window)
    print(f"  {system_labels[system]}: Created ON/OFF signal")

# Color schemes
colors = {
    'value': {'ON': '#2ecc71', 'OFF': '#e74c3c'},
    'risk': {'ON': '#3498db', 'OFF': '#e67e22'},
    'sentiment': {'ON': '#9b59b6', 'OFF': '#f39c12'},
    'insula': {'ON': '#34495e', 'OFF': '#95a5a6'},
    'control': {'ON': '#1abc9c', 'OFF': '#c0392b'}
}

# Function to create ON/OFF regime graph
def create_regime_graph(system_name, df, output_dir):
    """Create Risk-On/Risk-Off style time-series graph"""
    
    fig, ax = plt.subplots(figsize=(16, 7))
    
    signal = df[f'{system_name}_ON_OFF']
    dates = df['date']
    
    # Filled area plots
    ax.fill_between(dates, signal, 0, 
                     where=(signal >= 0), 
                     color=colors[system_name]['ON'], 
                     alpha=0.7, 
                     label=f'{system_labels[system_name]}-ON Regime',
                     interpolate=False,
                     step='mid')
    
    ax.fill_between(dates, signal, 0, 
                     where=(signal < 0), 
                     color=colors[system_name]['OFF'], 
                     alpha=0.7, 
                     label=f'{system_labels[system_name]}-OFF Regime',
                     interpolate=False,
                     step='mid')
    
    # Signal line
    ax.plot(dates, signal, color='black', linewidth=1.2, alpha=0.8, zorder=3)
    
    # Zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.9, zorder=4)
    
    # COVID period marker
    covid_start = df[df['period'] == 'Post-COVID']['date'].min()
    if pd.notna(covid_start):
        ax.axvline(x=covid_start, color='red', linestyle='--', linewidth=2.5, 
                   alpha=0.7, label='COVID Period Start', zorder=5)
        ax.text(covid_start, ax.get_ylim()[1]*0.9, 'COVID', 
                rotation=90, verticalalignment='top', fontsize=11, 
                color='red', fontweight='bold')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=13, fontweight='bold')
    ax.set_ylabel(f'{system_labels[system_name]} Regime Score\n(+1 = ON, -1 = OFF)', 
                  fontsize=13, fontweight='bold')
    ax.set_title(f'{system_labels[system_name]} System: ON vs OFF Regime Dynamics (Pre vs Post COVID)\n30-Day Rolling Average - XGBoost Analysis', 
                 fontsize=16, fontweight='bold', pad=20)
    
    ax.legend(loc='upper left', fontsize=11, framealpha=0.95, 
              edgecolor='black', fancybox=True, shadow=True)
    ax.grid(True, alpha=0.25, linestyle=':', linewidth=0.8, color='gray')
    ax.set_axisbelow(True)
    ax.set_ylim(-1.1, 1.1)
    
    # Reference lines
    ax.axhline(y=0.5, color='green', linestyle=':', linewidth=0.8, alpha=0.4)
    ax.axhline(y=-0.5, color='red', linestyle=':', linewidth=0.8, alpha=0.4)
    
    plt.xticks(rotation=45, ha='right')
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    
    output_file = output_dir / f'{system_name}_on_off_regime_xgboost.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  Saved: {output_file.name}")
    plt.close()

# Combined multi-panel figure
def create_combined_regime_graph(df, output_dir):
    """Create combined 5-panel figure"""
    
    fig, axes = plt.subplots(5, 1, figsize=(16, 18), sharex=True)
    
    for idx, system in enumerate(systems):
        ax = axes[idx]
        signal = df[f'{system}_ON_OFF']
        dates = df['date']
        
        # Fill areas
        ax.fill_between(dates, signal, 0, 
                         where=(signal >= 0), 
                         color=colors[system]['ON'], 
                         alpha=0.7, 
                         label=f'{system_labels[system]}-ON',
                         interpolate=False,
                         step='mid')
        
        ax.fill_between(dates, signal, 0, 
                         where=(signal < 0), 
                         color=colors[system]['OFF'], 
                         alpha=0.7, 
                         label=f'{system_labels[system]}-OFF',
                         interpolate=False,
                         step='mid')
        
        # Zero line
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1.2, alpha=0.7)
        
        # COVID marker
        covid_start = df[df['period'] == 'Post-COVID']['date'].min()
        if pd.notna(covid_start):
            ax.axvline(x=covid_start, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
        
        # Formatting
        ax.set_ylabel(f'{system_labels[system]}\nRegime', fontsize=11, fontweight='bold')
        ax.set_title(f'{system_labels[system]}-ON vs {system_labels[system]}-OFF', 
                     fontsize=12, fontweight='bold', pad=10)
        ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(-1.2, 1.2)
    
    axes[-1].set_xlabel('Date', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    fig.suptitle('Brain System ON/OFF Regime Dynamics: Pre vs Post COVID (XGBoost Analysis)\n30-Day Rolling Average - All 5 Systems', 
                 fontsize=15, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    
    output_file = output_dir / 'all_systems_on_off_regimes_xgboost.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n  Saved combined graph: {output_file.name}")
    plt.close()

# Generate graphs
print("\n" + "="*60)
print("GENERATING INDIVIDUAL ON/OFF REGIME GRAPHS (XGBOOST)")
print("="*60)

for system in systems:
    create_regime_graph(system, df, OUTPUT_DIR)

print("\n" + "="*60)
print("GENERATING COMBINED MULTI-PANEL GRAPH")
print("="*60)
create_combined_regime_graph(df, OUTPUT_DIR)

# Statistics
print("\n" + "="*60)
print("REGIME STATISTICS SUMMARY (XGBOOST)")
print("="*60)

summary_data = []
for system in systems:
    signal = df[f'{system}_ON_OFF']
    
    pre_signal = signal[df['period'] == 'Pre-COVID']
    pre_on_pct = (pre_signal > 0).sum() / len(pre_signal) * 100
    
    post_signal = signal[df['period'] == 'Post-COVID']
    post_on_pct = (post_signal > 0).sum() / len(post_signal) * 100
    
    change_pp = post_on_pct - pre_on_pct
    
    summary_data.append({
        'System': system_labels[system],
        'Pre_ON_%': round(pre_on_pct, 1),
        'Post_ON_%': round(post_on_pct, 1),
        'Change_pp': round(change_pp, 1),
        'Regime_Shift': 'More ON' if change_pp > 0 else 'More OFF'
    })

summary_df = pd.DataFrame(summary_data)
print("\n", summary_df.to_string(index=False))

summary_file = OUTPUT_DIR / 'regime_statistics_summary_xgboost.csv'
summary_df.to_csv(summary_file, index=False)
print(f"\nSaved summary: {summary_file.name}")

print("\n" + "="*60)
print("XGBOOST VISUALIZATION COMPLETE")
print("="*60)
print(f"\nOutput directory: {OUTPUT_DIR}")
print(f"Generated files:")
print(f"  - {len(systems)} individual regime graphs (including Insula)")
print(f"  - 1 combined 5-panel graph")
print(f"  - 1 summary statistics CSV")
