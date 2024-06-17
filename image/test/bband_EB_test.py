import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

def sharpe_ratio(data_list):
    no_tradable_days = len(data_list)
    print(no_tradable_days)
    SR = (no_tradable_days ** 0.5) * np.mean(data_list) / np.std(data_list)
    return SR

coin = "BTC"
exchange = "binance"

df_split = 1
test = 0 #0, 1, 2, ...
delay = 0

data = pd.read_csv(r"image/cleaned_data/exchange_balance_mixed_coins.csv")
data = data.dropna()

df_list = np.array_split(data, df_split)
test_set = df_list[test]
test_set = test_set.reset_index(drop=True)

print(test_set)

transaction_cost = 0.0006

z_thresh = 1.2
no_of_days_val = 40
periods = no_of_days_val * 24 * 6

df = pd.DataFrame()
df["timestamp"] = test_set["timestamp"]
df["price"] = test_set[coin + "_price"].shift(-delay)
df["exchange_balance"] = test_set[coin + '_' + exchange]
df = df.dropna()

df['MA'] = df['exchange_balance'].rolling(window = periods).mean()
df['std'] = df['exchange_balance'].rolling(window = periods).std()
df = df.iloc[periods - 1 : ]
df['z-score'] = np.where(df['std'] != 0, (df['exchange_balance'] - df['MA']) / df['std'], 0)
df['pos'] = 0
position = 0
for index, row in df.iterrows():
    if row['z-score'] >= z_thresh:
        df.at[index, 'pos'] = -1
        position = -1
    elif row['z-score'] <= -z_thresh:
        df.at[index, 'pos'] = 1
        position = 1
    elif row['z-score'] > 0 and position == -1:
        df.at[index, 'pos'] = position

    elif row['z-score'] < 0 and position == 1:
        df.at[index, 'pos'] = position
        
    else:
        df.at[index, 'pos'] = 0
        position = 0

df['pct_change'] = df['price'].pct_change()
df['price_change'] = df['price'].diff()
pos_shift = df['pos'].shift(1)
pos_shift.loc[:pos_shift.first_valid_index()][:-1] = 0 # first valid index should not be 0 -> add [:-1]
df['pos_t-1'] = pos_shift.dropna()

df['trade'] = df['pos'] - df['pos_t-1']
df['signal'] = abs(df['trade']) * df["exchange_balance"]
df['cost']  = abs(df['trade']) * transaction_cost
df['earnings'] = df['pos_t-1'] * df['price_change'] - df['cost'] * df['price']
df['pnl']   = df['pos_t-1'] * df['pct_change'] - df['cost']
df['cumulative earnings %']  = df['pnl'].cumsum()
df['cumulative earnings $']  = df['earnings'].cumsum()
df['dd']    = ( (df['cumulative earnings %']) - (df['cumulative earnings %']).cummax() )
df['underlying_cumu']  = df['pct_change'].cumsum()
df['underlying_dd']    = ( (df['underlying_cumu']) - (df['underlying_cumu']).cummax() )
df['upper_band'] = df['MA'] + z_thresh * df['std']
df['lower_band'] = df['MA'] - z_thresh * df['std']
df['control_experiment'] = df['price_change'].cumsum()
df = df.fillna(0)

short = (df['trade'] < 0).sum()
long = (df['trade'] > 0).sum()
no_of_transaction = long + short

acc_return = df['cumulative earnings $'][len(df)-1]
max_drawdown = df['dd'].min()

pnl = pd.DataFrame({'pnl': [sum(df['pnl'][i:i+144]) for i in range(0, len(df), 144)]})
remaining_data = df['pnl'].iloc[-len(df) % 144:]
pnl_remaining = pd.DataFrame({'pnl': [sum(remaining_data)]})
pnl = pd.concat([pnl, pnl_remaining], ignore_index=True)
SR = sharpe_ratio(pnl['pnl'])

print("*************************************************************************************************************")
print("z-score threshold: " + str(z_thresh))
print("number of days for computing moving average and std: " + str(no_of_days_val))
print("sharpe_ratio: " + str(SR))
print("accumulated return: " + str(acc_return))
print("number of transaction: " + str(no_of_transaction))
print("long-short ratio: " + str(long) + ':' + str(short))
print("max_drawdown: " + str(max_drawdown * 100) + "%")
print("*************************************************************************************************************")
df.to_csv('image/result/bt_exchange_balance_' + coin + '_' + exchange + '_delay_' + str(delay) + '_testing' + '.csv', index=False)
