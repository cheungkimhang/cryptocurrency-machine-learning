import pandas as pd

def EMA(indicator_list, period):
    EMA = indicator_list[-period]
    for current_value in indicator_list[-period + 1 :]:
        EMA = (current_value - EMA) * 2 / (period + 1) + EMA
    return EMA

BTC = pd.read_csv(r"image/raw_data/BTC.csv")

BTC = BTC[0:20000]
EMA_period = 14400

BTC['exchange_balance_EMA'] = ''
BTC['options_volume_put_call_ratio_EMA'] = ''
BTC['realized_volatility_1_week_EMA'] = ''
BTC['exchange_balance_normalized'] = ''
BTC['options_volume_put_call_ratio_normalized'] = ''
BTC['realized_volatility_1_week_normalized'] = ''
BTC['1_hour_price_change'] = ''
BTC['1_day_price_change'] = ''
BTC['5_day_price_change'] = ''


for index, row in BTC.iterrows():
    if index < EMA_period:
        pass
    else:
        previous_exchange_balance = list(BTC["exchange_balance"][index - EMA_period : index])
        row.iloc[BTC.columns.get_loc('exchange_balance_EMA')] = EMA(previous_exchange_balance, EMA_period)
        previous_options_volume_put_call_ratio = list(BTC["options_volume_put_call_ratio"][index - EMA_period : index])
        row.iloc[BTC.columns.get_loc('options_volume_put_call_ratio_EMA')] = EMA(previous_options_volume_put_call_ratio, EMA_period)
        previous_realized_volatility_1_week = list(BTC["realized_volatility_1_week"][index - EMA_period : index])
        row.iloc[BTC.columns.get_loc('realized_volatility_1_week_EMA')] = EMA(previous_realized_volatility_1_week, EMA_period)

        row.iloc[BTC.columns.get_loc('exchange_balance_normalized')] = (row.iloc[BTC.columns.get_loc('exchange_balance')] - row.iloc[BTC.columns.get_loc('exchange_balance_EMA')])/row.iloc[BTC.columns.get_loc('exchange_balance_EMA')]
        row.iloc[BTC.columns.get_loc('options_volume_put_call_ratio_normalized')] = (row.iloc[BTC.columns.get_loc('options_volume_put_call_ratio')] - row.iloc[BTC.columns.get_loc('options_volume_put_call_ratio_EMA')])/row.iloc[BTC.columns.get_loc('options_volume_put_call_ratio_EMA')]
        row.iloc[BTC.columns.get_loc('realized_volatility_1_week_normalized')] = (row.iloc[BTC.columns.get_loc('realized_volatility_1_week')] - row.iloc[BTC.columns.get_loc('realized_volatility_1_week_EMA')])/row.iloc[BTC.columns.get_loc('realized_volatility_1_week_EMA')]

        try:
            row.iloc[BTC.columns.get_loc("1_hour_price_change")] = (row.iloc[BTC.columns.get_loc("price_usd_close")].shift(-12) - row.iloc[BTC.columns.get_loc("price_usd_close")]) / row.iloc[BTC.columns.get_loc("price_usd_close")]
            row.iloc[BTC.columns.get_loc("1_day_price_change")] = (row.iloc[BTC.columns.get_loc("price_usd_close")].shift(-288) - row.iloc[BTC.columns.get_loc("price_usd_close")]) / row.iloc[BTC.columns.get_loc("price_usd_close")]
            row.iloc[BTC.columns.get_loc("5_day_price_change")] = (row.iloc[BTC.columns.get_loc("price_usd_close")].shift(-1440) - row.iloc[BTC.columns.get_loc("price_usd_close")]) / row.iloc[BTC.columns.get_loc("price_usd_close")]
        except:
            pass
        print(len(BTC)-index)

BTC = BTC.dropna()

BTC.to_csv('image/cleaned_data/BTC_EMA.csv', index=False)

print(BTC)
    
