"""
Create NDS Timeseries Data for ML-Based Figures
Uses ML-based activation predictions
"""

import pandas as pd

print("Creating NDS timeseries data from ML-based predictions...")

# Load ML-based data
df_combined = pd.read_csv('brain_activation_combined_xgboost_ML.csv')

# Separate by period
df_combined['date'] = pd.to_datetime(df_combined['date'])
covid_start = pd.to_datetime('2020-03-01').tz_localize('UTC').tz_convert('UTC+05:30')

# Create period label
df_combined['period'] = df_combined['date'].apply(
    lambda x: 'Pre-COVID' if x < covid_start else 'Post-COVID'
)

# Extract NDS (already computed as NDS_ML)
nds_timeseries = df_combined[['date', 'period', 'NDS_ML']].copy()
nds_timeseries = nds_timeseries.rename(columns={'NDS_ML': 'NDS'})

# Save
import os
os.makedirs('NDS_Distribution_Analysis', exist_ok=True)
nds_timeseries.to_csv('NDS_Distribution_Analysis/nds_timeseries_data_ML.csv', index=False)

print(f"✓ Saved: NDS_Distribution_Analysis/nds_timeseries_data_ML.csv")
print(f"  Total records: {len(nds_timeseries)}")
print(f"  Pre-COVID: {sum(nds_timeseries['period']=='Pre-COVID')}")
print(f"  Post-COVID: {sum(nds_timeseries['period']=='Post-COVID')}")
print(f"  NDS range: [{nds_timeseries['NDS'].min():.2f}, {nds_timeseries['NDS'].max():.2f}]")
