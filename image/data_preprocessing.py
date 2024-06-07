import pandas as pd

def EMA(indicator_list, period):
    EMA = indicator_list[-period]
    for current_value in indicator_list[-period + 1 :]:
        EMA = (current_value - EMA) * 2 / (period + 1) + EMA
    return EMA

def update_row(df, row, EMA_period):
    print(row.name)
    if row.name < EMA_period:
        return row
    else:
        row['exchange_balance_EMA'] = EMA(list(df["exchange_balance"][row.name - EMA_period : row.name]), EMA_period)
        row['options_volume_put_call_ratio_EMA'] = EMA(list(df["options_volume_put_call_ratio"][row.name - EMA_period : row.name]), EMA_period)
        row['realized_volatility_1_week_EMA'] = EMA(list(df["realized_volatility_1_week"][row.name - EMA_period : row.name]), EMA_period)

        row['exchange_balance_normalized'] = (row['exchange_balance'] - row['exchange_balance_EMA']) / row['exchange_balance_EMA']
        row['options_volume_put_call_ratio_normalized'] = (row['options_volume_put_call_ratio'] - row['options_volume_put_call_ratio_EMA']) / row['options_volume_put_call_ratio_EMA']
        row['realized_volatility_1_week_normalized'] = (row['realized_volatility_1_week'] - row['realized_volatility_1_week_EMA']) / row['realized_volatility_1_week_EMA']

        try:
            row['1_hour_price_change'] = (df['price_usd_close'].iloc[row.name + 12] - row['price_usd_close']) / row['price_usd_close']
            row['1_day_price_change'] = (df['price_usd_close'].iloc[row.name + 288] - row['price_usd_close']) / row['price_usd_close']
            row['5_day_price_change'] = (df['price_usd_close'].iloc[row.name + 1440] - row['price_usd_close']) / row['price_usd_close']

        except:
            row['1_hour_price_change'] = 0
            row['1_day_price_change'] = 0
            row['5_day_price_change'] = 0

        return row
    
BTC = pd.read_csv(r"image/raw_data/BTC.csv")
print(len(BTC))
BTC = BTC.dropna()
BTC = BTC.reset_index(drop=True)
print(len(BTC))

print(BTC)
EMA_period = 14400

BTC['exchange_balance_EMA'] = 0
BTC['options_volume_put_call_ratio_EMA'] = 0
BTC['realized_volatility_1_week_EMA'] = 0
BTC['exchange_balance_normalized'] = 0
BTC['options_volume_put_call_ratio_normalized'] = 0
BTC['realized_volatility_1_week_normalized'] = 0
BTC['1_hour_price_change'] = 0
BTC['1_day_price_change'] = 0
BTC['5_day_price_change'] = 0

# Apply the update_row function to each row of the DataFrame
BTC = BTC.apply(lambda row: update_row(BTC, row, EMA_period), axis=1)

# Remove all the rows with 0
BTC = BTC.loc[(BTC != 0).all(axis=1)]

# Save the cleaned DataFrame to a CSV file
BTC.to_csv('image/cleaned_data/BTC_EMA.csv', index=False)

# Print the updated DataFrame
print(BTC)