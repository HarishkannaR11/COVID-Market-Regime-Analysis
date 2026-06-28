"""Quick check: Is Risk actually dominant in Post-COVID?"""
import pandas as pd
import numpy as np

# Load brain activation data
pre = pd.read_csv('brain_activation_pre_covid.csv')
post = pd.read_csv('brain_activation_post_covid.csv')

print('='*70)
print('BRAIN SYSTEM ACTIVATION RATES (% of days active)')
print('='*70)
print(f"{'System':<20} {'Pre-COVID':>12} {'Post-COVID':>12} {'Change':>12}")
print('-'*70)

systems = [
    ('value_active', 'Value System'),
    ('risk_active', 'Risk System'),
    ('sentiment_active', 'Sentiment System'),
    ('insula_active', 'Anomaly Detection'),
    ('control_active', 'Control System')
]

activation_data = []
for col, name in systems:
    pre_rate = pre[col].mean() * 100
    post_rate = post[col].mean() * 100
    change = post_rate - pre_rate
    activation_data.append((name, pre_rate, post_rate, change))
    print(f'{name:<20} {pre_rate:>11.1f}% {post_rate:>11.1f}% {change:>+11.1f}%')

print('='*70)

# NDS Formula: Value - Risk + Sentiment
# Negative NDS means: Risk > Value + Sentiment
print('\nNDS INTERPRETATION')
print('='*70)
print('Formula: NDS = Value - Risk + Sentiment')
print('\nPre-COVID:  NDS ≈ 0.00  → Balanced')
print('Post-COVID: NDS = -2.01 → NEGATIVE')
print('\nNegative NDS means: Risk > (Value + Sentiment)')
print('='*70)

# Check what actually changed
print('\nWHAT CHANGED?')
print('='*70)
value_change = activation_data[0][3]
risk_change = activation_data[1][3]
sentiment_change = activation_data[2][3]

print(f'Value activation:     {value_change:+.1f}%')
print(f'Risk activation:      {risk_change:+.1f}%')
print(f'Sentiment activation: {sentiment_change:+.1f}%')

if risk_change > 0:
    print('\n→ Risk system became MORE active')
elif risk_change < 0:
    print('\n→ Risk system became LESS active')
    
if value_change < 0:
    print('→ Value system became LESS active')
elif value_change > 0:
    print('→ Value system became MORE active')
    
print('\nCONCLUSION:')
if risk_change > value_change:
    print('✓ Risk increased more than Value → TRUE RISK DOMINANCE')
else:
    interpretation = 'Risk decreased LESS than Value' if risk_change < 0 else 'Complex change'
    print(f'? {interpretation} → RELATIVE CHANGE, not absolute dominance')
print('='*70)
