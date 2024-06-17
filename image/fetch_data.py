from load_data import get_data
import pandas as pd

get_data = get_data()

symbol = "BNB"
interval_glassnode = "10m"
exchange = "binance"

hash_rate_mean = get_data.get_data_from_glassnode(symbol, "https://api.glassnode.com/v1/metrics/distribution/balance_exchanges_pit", interval_glassnode, exchange = exchange)

hash_rate_mean.to_csv('image/raw_data/' + symbol + '_' + interval_glassnode + '_' + exchange + '_exchange_balance.csv', index=False)