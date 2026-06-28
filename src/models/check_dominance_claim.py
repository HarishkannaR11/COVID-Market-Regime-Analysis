"""
Check: Can we claim "Value is dominant and Risk is second dominant"?
"""
import pandas as pd
import numpy as np

# Load brain activation data
pre = pd.read_csv('brain_activation_pre_covid.csv')
post = pd.read_csv('brain_activation_post_covid.csv')

print("="*80)
print("BRAIN SYSTEM DOMINANCE ANALYSIS")
print("="*80)

systems = [
    ('value_active', 'Value System'),
    ('risk_active', 'Risk System'),
    ('sentiment_active', 'Sentiment System'),
    ('insula_active', 'Anomaly Detection'),
    ('control_active', 'Control System')
]

print("\nACTIVATION RATES (% of days each system is active)")
print("-"*80)

# Pre-COVID ranking
pre_rates = []
for col, name in systems:
    rate = pre[col].mean() * 100
    pre_rates.append((name, rate))

pre_rates_sorted = sorted(pre_rates, key=lambda x: x[1], reverse=True)

print("\nPRE-COVID RANKING:")
for i, (name, rate) in enumerate(pre_rates_sorted, 1):
    print(f"  {i}. {name:<20} {rate:>6.1f}%")

# Post-COVID ranking
post_rates = []
for col, name in systems:
    rate = post[col].mean() * 100
    post_rates.append((name, rate))

post_rates_sorted = sorted(post_rates, key=lambda x: x[1], reverse=True)

print("\nPOST-COVID RANKING:")
for i, (name, rate) in enumerate(post_rates_sorted, 1):
    print(f"  {i}. {name:<20} {rate:>6.1f}%")

print("\n" + "="*80)
print("CAN YOU CLAIM 'VALUE IS DOMINANT, RISK IS SECOND DOMINANT'?")
print("="*80)

# Check Post-COVID (the period of interest)
post_dict = dict(post_rates_sorted)

value_rank = [i for i, (name, _) in enumerate(post_rates_sorted, 1) if name == 'Value System'][0]
risk_rank = [i for i, (name, _) in enumerate(post_rates_sorted, 1) if name == 'Risk System'][0]

print(f"\nPost-COVID Rankings:")
print(f"  Value System: #{value_rank} ({post_dict['Value System']:.1f}%)")
print(f"  Risk System:  #{risk_rank} ({post_dict['Risk System']:.1f}%)")

print("\n" + "-"*80)
if value_rank == 1 and risk_rank == 2:
    print("✓ YES - Your claim is SUPPORTED!")
    print("  Value is the most active system")
    print("  Risk is the second most active system")
elif value_rank == 1:
    print(f"✗ PARTIALLY - Value IS dominant (#{value_rank})")
    print(f"  BUT Risk is #{risk_rank}, not #2")
    print(f"  Second dominant is: {post_rates_sorted[1][0]}")
elif risk_rank == 2:
    print(f"✗ PARTIALLY - Risk IS second (#{risk_rank})")
    print(f"  BUT Value is #{value_rank}, not #1")
    print(f"  Most dominant is: {post_rates_sorted[0][0]}")
else:
    print(f"✗ NO - Your claim is NOT supported")
    print(f"  Value is #{value_rank}, not #1")
    print(f"  Risk is #{risk_rank}, not #2")
    print(f"\n  Most dominant: {post_rates_sorted[0][0]} ({post_rates_sorted[0][1]:.1f}%)")
    print(f"  2nd dominant:  {post_rates_sorted[1][0]} ({post_rates_sorted[1][1]:.1f}%)")

print("\n" + "="*80)
print("ACCURATE CLAIM YOU CAN MAKE:")
print("="*80)

print(f"\n'{post_rates_sorted[0][0]} is the dominant system in Post-COVID period,")
print(f" with {post_rates_sorted[0][1]:.1f}% activation, followed by {post_rates_sorted[1][0]}")
print(f" at {post_rates_sorted[1][1]:.1f}%.'")

print("\n" + "-"*80)
print("ALTERNATIVE FRAMING:")
print("-"*80)

# Check if value is in top 3
if value_rank <= 3:
    print(f"\n✓ You CAN claim: 'Value is among the top {value_rank} most active systems'")
    
# Check what value/risk relationship is
value_rate = post_dict['Value System']
risk_rate = post_dict['Risk System']

if value_rate > risk_rate:
    ratio = value_rate / risk_rate
    print(f"✓ You CAN claim: 'Value system is {ratio:.1f}x more active than Risk")
    print(f"  (Value: {value_rate:.1f}%, Risk: {risk_rate:.1f}%)'")

# Days active comparison
print(f"\n✓ You CAN claim: 'Value system activates on {value_rate:.1f}% of trading days,")
print(f"  while Risk activates on only {risk_rate:.1f}% of days in Post-COVID period'")

print("\n" + "="*80)
