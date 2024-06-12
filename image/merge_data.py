import pandas as pd

price = pd.read_csv("image/raw_data/BTC_10m_price_usd_close.csv")
binance = pd.read_csv("image/raw_data/BTC_10m_binance_exchange_balance.csv")
bybit = pd.read_csv("image/raw_data/BTC_10m_bybit_exchange_balance.csv")
okex = pd.read_csv("image/raw_data/BTC_10m_okex_exchange_balance.csv")

binance = binance.rename(columns={'value': 'binance'})
bybit = bybit.rename(columns={'value': 'bybit'})
okex = okex.rename(columns={'value': 'okex'})

merged_df = pd.DataFrame()
merged_df["timestamp"] = price["timestamp"]
merged_df["price"] = price["value"]

merged_df = pd.merge(merged_df, binance, on="timestamp", how="left")
merged_df = pd.merge(merged_df, bybit, on="timestamp", how="left")
merged_df = pd.merge(merged_df, okex, on="timestamp", how="left")

merged_df = merged_df.dropna()
merged_df.to_csv("image/cleaned_data/BTC_exchange_balance_10m.csv", index = False)