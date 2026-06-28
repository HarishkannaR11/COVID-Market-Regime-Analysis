"""
ON vs OFF Time-Series Regime Visualization
Creates Risk-On/Risk-Off style graphs for all cognitive systems

Generates filled area plots showing regime dominance and switching over time
for Value, Risk, Sentiment, Insula, and Control systems.
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
plt.rcParams['font.weight'] = 'normal'

# Define paths
DATA_PATH = Path(r'c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels\brain_activation_combined_xgboost.csv')
OUTPUT_DIR = Path(r'c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels\ON_OFF_Regime_Graphs')

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

print(f"Data loaded: {len(df)} days, Period: {df['Date'].min()} to {df['Date'].max()}")

# Define systems (XGBoost has 5 systems including Insula)
systems = ['Value', 'Risk', 'Sentiment', 'Insula', 'Control']

# Note: The CSV has activation columns for all 5 systems
print("\nSystems analyzed:", systems)

# Create binary ON/OFF states for each system
# XGBoost data is already binary (0 or 1), so we convert directly to +1/-1 for visualization
rolling_window = 30  # 30-day rolling window for sharper spikes

def create_on_off_signal(series, window=30):
    """
    Create ON/OFF signal with rolling window smoothing
    XGBoost activations are binary: 1 (active) → +1 (ON), 0 (inactive) → -1 (OFF)
    Uses shorter window for clearer regime spikes
    """
    # Convert binary 0/1 to -1/+1 for visualization
    binary = np.where(series == 1, 1, -1)
    # Apply rolling mean for smoothing (shorter window = sharper transitions)
    smoothed = pd.Series(binary).rolling(window=window, min_periods=1, center=False).mean()
    return smoothed

# Process each system
print(f"\nCreating ON/OFF signals with {rolling_window}-day rolling window (shorter window = sharper spikes)...")

for system in systems:
    if system in df.columns:
        df[f'{system}_ON_OFF'] = create_on_off_signal(df[system], window=rolling_window)
        print(f"  {system}: Created ON/OFF signal")
    else:
        print(f"  {system}: Column not found")

# Add COVID period markers
df['COVID_Period'] = df['period'].map({'Pre-COVID': 0, 'Post-COVID': 1})

# Define color schemes (matching Risk-On/Risk-Off style)
colors = {
    'Value': {'ON': '#2ecc71', 'OFF': '#e74c3c'},      # Green/Red
    'Risk': {'ON': '#3498db', 'OFF': '#e67e22'},       # Blue/Orange  
    'Sentiment': {'ON': '#9b59b6', 'OFF': '#f39c12'},  # Purple/Yellow
    'Control': {'ON': '#1abc9c', 'OFF': '#c0392b'},    # Teal/DarkRed
    'Insula': {'ON': '#34495e', 'OFF': '#95a5a6'}      # DarkGray/LightGray
}

# Function to create ON/OFF regime graph with sharper spikes
def create_regime_graph(system_name, df, output_dir):
    """
    Create Risk-On/Risk-Off style time-series graph for a brain system
    Enhanced visualization with sharper regime transitions
    """
    if f'{system_name}_ON_OFF' not in df.columns:
        print(f"Skipping {system_name} - no ON/OFF data")
        return
    
    fig, ax = plt.subplots(figsize=(16, 7))
    
    # Get ON/OFF signal
    signal = df[f'{system_name}_ON_OFF']
    dates = df['Date']
    
    # Create filled area plot with edge lines for sharper appearance
    # Positive values = ON regime (fill above zero)
    ax.fill_between(dates, signal, 0, 
                     where=(signal >= 0), 
                     color=colors[system_name]['ON'], 
                     alpha=0.7, 
                     label=f'{system_name}-ON Regime',
                     interpolate=False,
                     step='mid')
    
    # Negative values = OFF regime (fill below zero)
    ax.fill_between(dates, signal, 0, 
                     where=(signal < 0), 
                     color=colors[system_name]['OFF'], 
                     alpha=0.7, 
                     label=f'{system_name}-OFF Regime',
                     interpolate=False,
                     step='mid')
    
    # Add signal line for clarity
    ax.plot(dates, signal, color='black', linewidth=1.2, alpha=0.8, zorder=3)
    
    # Add zero line (thicker for emphasis)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.9, zorder=4)
    
    # Add COVID period vertical line
    covid_start = df[df['period'] == 'Post-COVID']['Date'].min()
    if pd.notna(covid_start):
        ax.axvline(x=covid_start, color='red', linestyle='--', linewidth=2.5, 
                   alpha=0.7, label='COVID Period Start', zorder=5)
        # Add text annotation
        ax.text(covid_start, ax.get_ylim()[1]*0.9, 'COVID', 
                rotation=90, verticalalignment='top', fontsize=11, 
                color='red', fontweight='bold')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=13, fontweight='bold')
    ax.set_ylabel(f'{system_name} Regime Score\n(+1 = ON, -1 = OFF)', 
                  fontsize=13, fontweight='bold')
    ax.set_title(f'{system_name} System: ON vs OFF Regime Dynamics (Pre vs Post COVID)\n30-Day Rolling Average', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Enhanced legend
    ax.legend(loc='upper left', fontsize=11, framealpha=0.95, 
              edgecolor='black', fancybox=True, shadow=True)
    
    # Grid for readability
    ax.grid(True, alpha=0.25, linestyle=':', linewidth=0.8, color='gray')
    ax.set_axisbelow(True)
    
    # Set y-axis limits for consistency
    ax.set_ylim(-1.1, 1.1)
    
    # Add horizontal reference lines
    ax.axhline(y=0.5, color='green', linestyle=':', linewidth=0.8, alpha=0.4)
    ax.axhline(y=-0.5, color='red', linestyle=':', linewidth=0.8, alpha=0.4)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    # Add subtle background
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    
    # Save with high quality
    output_file = output_dir / f'{system_name.lower()}_on_off_regime.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  Saved: {output_file.name}")
    plt.close()

# Create multi-panel figure with all systems
def create_combined_regime_graph(df, output_dir):
    """
    Create combined multi-panel figure with all systems
    """
    available_systems = [s for s in systems if f'{s}_ON_OFF' in df.columns]
    n_systems = len(available_systems)
    
    fig, axes = plt.subplots(n_systems, 1, figsize=(16, 3.5 * n_systems), sharex=True)
    
    if n_systems == 1:
        axes = [axes]
    
    for idx, system in enumerate(available_systems):
        ax = axes[idx]
        signal = df[f'{system}_ON_OFF']
        dates = df['Date']
        
        # Fill areas
        ax.fill_between(dates, signal, 0, 
                         where=(signal >= 0), 
                         color=colors[system]['ON'], 
                         alpha=0.6, 
                         label=f'{system}-ON',
                         interpolate=True)
        
        ax.fill_between(dates, signal, 0, 
                         where=(signal < 0), 
                         color=colors[system]['OFF'], 
                         alpha=0.6, 
                         label=f'{system}-OFF',
                         interpolate=True)
        
        # Zero line
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1.2, alpha=0.7)
        
        # COVID period shading
        covid_start = df[df['period'] == 'Post-COVID']['Date'].min()
        if pd.notna(covid_start):
            ax.axvspan(covid_start, dates.max(), alpha=0.08, color='gray')
        
        # Formatting
        ax.set_ylabel(f'{system}\nRegime', fontsize=11, fontweight='bold')
        ax.set_title(f'{system}-ON vs {system}-OFF', fontsize=12, fontweight='bold', pad=10)
        ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(-1.2, 1.2)
    
    # X-axis label only on bottom
    axes[-1].set_xlabel('Date', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    # Overall title
    fig.suptitle('Brain System ON/OFF Regime Dynamics: Pre vs Post COVID (XGBoost)\n(30-Day Rolling Average)', 
                 fontsize=15, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    
    # Save
    output_file = output_dir / 'all_systems_on_off_regimes.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n  Saved combined graph: {output_file.name}")
    plt.close()

# Generate individual graphs
print("\n" + "="*60)
print("GENERATING INDIVIDUAL ON/OFF REGIME GRAPHS")
print("="*60)

for system in systems:
    create_regime_graph(system, df, OUTPUT_DIR)

# Generate combined multi-panel graph
print("\n" + "="*60)
print("GENERATING COMBINED MULTI-PANEL GRAPH")
print("="*60)
create_combined_regime_graph(df, OUTPUT_DIR)

# Create summary statistics
print("\n" + "="*60)
print("REGIME STATISTICS SUMMARY")
print("="*60)

summary_data = []
for system in systems:
    if f'{system}_ON_OFF' in df.columns:
        signal = df[f'{system}_ON_OFF']
        
        # Pre-COVID stats
        pre_signal = signal[df['period'] == 'Pre-COVID']
        pre_on_pct = (pre_signal > 0).sum() / len(pre_signal) * 100
        
        # Post-COVID stats
        post_signal = signal[df['period'] == 'Post-COVID']
        post_on_pct = (post_signal > 0).sum() / len(post_signal) * 100
        
        # Change
        change_pp = post_on_pct - pre_on_pct
        
        summary_data.append({
            'System': system,
            'Pre_ON_%': round(pre_on_pct, 1),
            'Post_ON_%': round(post_on_pct, 1),
            'Change_pp': round(change_pp, 1),
            'Regime_Shift': 'More ON' if change_pp > 0 else 'More OFF'
        })

summary_df = pd.DataFrame(summary_data)
print("\n", summary_df.to_string(index=False))

# Save summary
summary_file = OUTPUT_DIR / 'regime_statistics_summary.csv'
summary_df.to_csv(summary_file, index=False)
print(f"\nSaved summary: {summary_file.name}")

print("\n" + "="*60)
print("VISUALIZATION COMPLETE")
print("="*60)
print(f"\nOutput directory: {OUTPUT_DIR}")
print(f"Generated files:")
print(f"  - {len(systems)} individual regime graphs")
print(f"  - 1 combined multi-panel graph")
print(f"  - 1 summary statistics CSV")
