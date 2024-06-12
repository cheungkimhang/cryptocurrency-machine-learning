import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

def sharpe_ratio(data_list):
        SR = (365 ** 0.5) * np.mean(data_list) / np.std(data_list)
        return SR

coin = "BTC"
exchange = "okex"
test = 1
data = pd.read_csv(r"image/cleaned_data/BTC_exchange_balance_10m.csv")
data = data.dropna()

df_list = np.array_split(data, 2)
test_set = df_list[test]
test_set = test_set.reset_index(drop=True)

transaction_cost = 0.0006

best_SR = 0

z_threshes = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
no_of_days = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

heat_map_dict = {'z_threshes': [], 'no_of_days': [], 'Strategy_Sharpe_Ratio': []}

SR_matrix = np.zeros((len(z_threshes), len(no_of_days)))

for i in range(len(z_threshes)):
    for j in range(len(no_of_days)):
               
        z_thresh = z_threshes[i]
        no_of_days_val = no_of_days[j]
        periods = no_of_days_val * 24 * 6

        heat_map_dict['z_threshes'].append(z_thresh)
        heat_map_dict['no_of_days'].append(no_of_days_val)

        print(z_thresh, ", ", no_of_days_val)

        df = pd.DataFrame()
        df["timestamp"] = test_set["timestamp"]
        df["price"] = test_set["price"]
        df["exchange_balance"] = test_set[exchange]

        df['SMA'] = df['exchange_balance'].rolling(window = periods).mean()
        df['std'] = df['exchange_balance'].rolling(window = periods).std()
        df = df.iloc[periods - 1 : ]
        df['z-score'] = np.where(df['std'] != 0, (df['exchange_balance'] - df['SMA']) / df['std'], 0)
        df['pos'] = 0
        position = 0
        for index, row in df.iterrows():
            if row['z-score'] > z_thresh:
                df.at[index, 'pos'] = -1
                position = -1
            elif row['z-score'] < -z_thresh:
                df.at[index, 'pos'] = 1
                position = 1
            elif row['z-score'] > 0 and position == -1:
                df.at[index, 'pos'] = -1
                position = -1
            elif row['z-score'] < 0 and position == 1:
                df.at[index, 'pos'] = 1
                position = 1
            else:
                df.at[index, 'pos'] = 0
                position = 0



        df['pct_change'] = df['price'].pct_change()
        df['price_change'] = df['price'].diff()
        pos_shift = df['pos'].shift(1)
        pos_shift.loc[:pos_shift.first_valid_index()][:-1] = 0 # first valid index should not be 0 -> add [:-1]
        df['pos_t-1'] = pos_shift.dropna()

        df['trade'] = df['pos'] - df['pos_t-1']
        df['cost']  = abs(df['trade']) * transaction_cost
        df['earnings'] = df['pos_t-1'] * df['price_change'] - df['cost'] * df['price']
        df['pnl']   = df['pos_t-1'] * df['pct_change'] - df['cost']
        df['cumulative earnings %']  = df['pnl'].cumsum()
        df['cumulative earnings $']  = df['earnings'].cumsum()
        df['dd']    = ( (df['cumulative earnings %']) - (df['cumulative earnings %']).cummax() )
        df['underlying_cumu']  = df['pct_change'].cumsum()
        df['underlying_dd']    = ( (df['underlying_cumu']) - (df['underlying_cumu']).cummax() )
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
        
        heat_map_dict['Strategy_Sharpe_Ratio'].append(SR)

        if SR > best_SR:
            best_SR = SR
            print("*************************************************************************************************************")
            print("z-score threshold: " + str(z_thresh))
            print("number of days for computing moving average and std: " + str(no_of_days_val))
            print("sharpe_ratio: " + str(SR))
            print("accumulated return: " + str(acc_return))
            print("number of transaction: " + str(no_of_transaction))
            print("long-short ratio: " + str(long) + ':' + str(short))
            print("max_drawdown: " + str(max_drawdown * 100) + "%")
            print("*************************************************************************************************************")
            df.to_csv('image/result/bt_exchange_balance_' + coin + '_' + exchange + '_' + str(test) + '.csv', index=False)
        else:
            print(SR)

# Create the heatmap
heat_map = pd.DataFrame(heat_map_dict)
heat_map = heat_map.squeeze(True)
plt.figure(figsize=(12, 8))

heatmap_temp = heat_map.pivot(index="z_threshes", columns="no_of_days", values="Strategy_Sharpe_Ratio").reindex(index=heat_map["z_threshes"].unique()[::-1])

# Create the heatmap
heatmap = sns.heatmap(heatmap_temp, cmap="RdBu_r")

# Set the title and axis labels
heatmap.set_title('Heatmap of Strategy_Sharpe_Ratio', fontsize=14)
heatmap.set_ylabel('longPeriod', fontsize=12)
heatmap.set_xlabel('shortPeriod', fontsize=12)

plt.savefig('image/result/heatmap_bband_' + coin + '_' + exchange + '_' + str(test) + '.png')
plt.show()



'''
fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(df['timestamp'], df['exchange_balance'], label='exchange balance')
ax.plot(df['timestamp'], df['SMA'], label='SMA')
ax.plot(df['timestamp'], df['upper_band'], label='Upper Band')
ax.plot(df['timestamp'], df['lower_band'], label='Lower Band')

# Add the mini bar chart for price

ax2 = ax.twinx()
ax2.bar(df['timestamp'], df['price'], color='r', alpha=0.5, width=0.2)
ax2.set_ylabel('Price (USD)', color='r')
ax2.tick_params('y', colors='r')
ax2.format_ydata = lambda x: f'${x:.2f}'
ax2.yaxis.set_major_formatter(FormatStrFormatter('$%.2f'))

ax.set_xlabel('Time')
ax.set_ylabel('exchange balance')
ax.tick_params(axis='x', rotation=45)

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.suptitle('Bitcoin Price with Bollinger Bands')
plt.savefig('bollinger_bands.png', dpi=300)
plt.show()
'''