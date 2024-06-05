from load_data import get_data
import pandas as pd

get_data = get_data()

symbol = "BTC"
interval_glassnode = "10m"

hash_rate_mean = get_data.get_data_from_glassnode(symbol, "https://api.glassnode.com/v1/metrics/mining/hash_rate_mean", interval_glassnode)

hash_rate_mean.to_csv('image/raw_data/' + symbol + '_' + interval_glassnode + '_hash_rate_mean.csv', index=False)