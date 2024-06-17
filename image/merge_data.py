import pandas as pd

BTC_price = pd.read_csv("image/raw_data/BTC_10m_price_usd_close.csv")
ETH_price = pd.read_csv("image/raw_data/ETH_10m_price_usd_close.csv")

BTC_binance = pd.read_csv("image/raw_data/BTC_10m_binance_exchange_balance.csv")
ETH_binance = pd.read_csv("image/raw_data/ETH_10m_exchange_balance.csv")

merged_df = pd.DataFrame()
merged_df["timestamp"] = BTC_price["timestamp"]
merged_df["BTC_price"] = BTC_price["value"]

merged_df = pd.merge(merged_df, ETH_price, on="timestamp", how="left")
merged_df = pd.merge(merged_df, BTC_binance, on="timestamp", how="left")
merged_df = pd.merge(merged_df, ETH_binance, on="timestamp", how="left")
merged_df = merged_df.dropna()

merged_df.to_csv("image/cleaned_data/exchange_balance_mixed_coins.csv", index = False)