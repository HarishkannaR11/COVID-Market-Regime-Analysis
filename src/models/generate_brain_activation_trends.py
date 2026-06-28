"""
Generate Brain System Activation Trend graphs (30-Day Rolling)
using XGBoost ML predictions (random split) from pre/post COVID datasets.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent.parent.parent  # NDS-ImprovedModels/
OUT  = Path(__file__).parent                # Brain_activation/

# -------------------------------------------------------------------
# Load data
# -------------------------------------------------------------------
pre  = pd.read_csv(BASE / 'brain_activation_pre_covid_ML.csv')
post = pd.read_csv(BASE / 'brain_activation_post_covid_ML.csv')

pre['date']  = pd.to_datetime(pre['date'],  utc=True)
post['date'] = pd.to_datetime(post['date'], utc=True)

# -------------------------------------------------------------------
# System definitions  (ML columns + colours)
# -------------------------------------------------------------------
SYSTEMS = {
    'Value':              ('value_active_ml',     '#e74c3c'),
    'Risk':               ('risk_active_ml',      '#f39c12'),
    'Sentiment':          ('sentiment_active_ml', '#27ae60'),
    'Anomaly Detection':  ('insula_active_ml',    '#9b59b6'),
    'Control':            ('control_active_ml',   '#3498db'),
}

# -------------------------------------------------------------------
# Plot function
# -------------------------------------------------------------------
def plot_activation(df: pd.DataFrame, title: str, outpath: Path) -> None:
    fig, ax = plt.subplots(figsize=(36, 8))

    for label, (col, color) in SYSTEMS.items():
        rolling = (
            df.set_index('date')[col]
            .rolling('30D')
            .mean() * 100
        )
        ax.plot(rolling.index, rolling.values,
                label=label, color=color, linewidth=2)

    ax.set_title(title, fontsize=24, fontweight='bold', pad=12)
    ax.set_xlabel('Date', fontsize=20, fontweight='bold')
    ax.set_ylabel('Activation Frequency (%)', fontsize=20, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.tick_params(axis='both', labelsize=17)
    ax.grid(True, axis='both', linestyle='--', alpha=0.4)
    ax.legend(fontsize=18, loc='upper right', framealpha=0.9)
    ax.set_facecolor('#f8f9fa')
    plt.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {outpath.name}')


# -------------------------------------------------------------------
# Generate individual charts
# -------------------------------------------------------------------
plot_activation(pre,
                'Pre-COVID: Brain System Activation Over Time (30-Day Rolling) [XGBoost ML]',
                OUT / 'activation_trends_pre_covid.png')

plot_activation(post,
                'Post-COVID: Brain System Activation Over Time (30-Day Rolling) [XGBoost ML]',
                OUT / 'activation_trends_post_covid.png')

# -------------------------------------------------------------------
# Combine: Pre above, Post below
# -------------------------------------------------------------------
img_pre  = Image.open(OUT / 'activation_trends_pre_covid.png')
img_post = Image.open(OUT / 'activation_trends_post_covid.png')

w      = max(img_pre.width, img_post.width)
pre_r  = img_pre.resize( (w, int(img_pre.height  * w / img_pre.width)),  Image.LANCZOS)
post_r = img_post.resize((w, int(img_post.height * w / img_post.width)), Image.LANCZOS)

combined = Image.new('RGB', (w, pre_r.height + post_r.height), (255, 255, 255))
combined.paste(pre_r,  (0, 0))
combined.paste(post_r, (0, pre_r.height))
combined.save(OUT / 'brain_activation_combined.png', dpi=(150, 150))
print('Saved: brain_activation_combined.png')
