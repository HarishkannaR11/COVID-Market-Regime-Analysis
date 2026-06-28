"""
ALTERNATIVE APPROACH: NO DATA LEAKAGE
Uses absolute thresholds instead of percentile-based thresholds
"""

def detect_brain_activation_no_leakage(df, system_name):
    """
    Detect brain activation using ABSOLUTE thresholds only
    No data leakage - doesn't use statistics from the dataset
    """
    activation = pd.Series(False, index=df.index)
    
    if system_name == 'value':
        # RSI extremes (standard oversold/overbought)
        # Large absolute returns (>1.5% daily)
        activation = (
            (df['rsi'] > 65) | (df['rsi'] < 35) |  
            (abs(df['daily_return']) > 0.015) |  # 1.5% daily return
            (abs(df['momentum_30d']) > 0.05)     # 5% monthly momentum
        )
    
    elif system_name == 'risk':
        # High volatility (>1.5% daily) OR negative returns
        activation = (
            (df['volatility_20d'] > 0.015) |     # 1.5% daily volatility
            (df['daily_return'] < -0.01)         # -1% daily return
        )
    
    elif system_name == 'sentiment':
        # Deviation from moving averages (already absolute)
        activation = (
            (abs(df['price_to_ma50']) > 0.03) |  # 3% from MA-50
            (abs(df['price_to_ma200']) > 0.05)   # 5% from MA-200
        )
    
    elif system_name == 'insula':
        # Absolute gap/range/volume thresholds
        activation = (
            (abs(df['gap_open']) > 0.01) |       # 1% gap
            (df['intraday_range'] > 0.015) |     # 1.5% intraday range
            (df['volume_spike'] > 1.3)           # 1.3x volume
        )
    
    return activation.astype(int)


# ANALYSIS OF CURRENT APPROACH:
# ==============================
# Current percentile approach has MILD leakage because:
# 
# 1. Activation labels are created BEFORE train/test split
# 2. Percentiles are calculated on full Pre-COVID or Post-COVID datasets
# 3. When you split 80/20, test set labels use statistics that include test data
#
# HOWEVER, the leakage is LIMITED because:
# - Percentiles are calculated per regime (Pre vs Post separately)
# - The leakage is only in the activation LABELS, not the features
# - XGBoost learns patterns, not the thresholds themselves
# - Cross-validation still gives realistic performance estimates
#
# RECOMMENDATION:
# - If using percentiles: Calculate on TRAINING data only, apply to test
# - OR use absolute thresholds (no dataset statistics needed)
# - Current approach is acceptable for descriptive research but not ideal for prediction
