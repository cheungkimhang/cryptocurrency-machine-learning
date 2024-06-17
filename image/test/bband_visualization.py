import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

coin = "bTC"
df = pd.read_csv(r"image\result\bt_exchange_balance_BTC_binance_delay_0_testing.csv")
df = df.iloc[len(df)//3 * 2 : ]
num_rows = len(df)
keep_rows = list(range(0, num_rows, 144))
df = df.iloc[keep_rows]

fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(df['timestamp'], df['exchange_balance'], color='red', label='binance exchange balance')
ax.plot(df['timestamp'], df['MA'], color='blue', label='Middle Band')
ax.plot(df['timestamp'], df['upper_band'], color='black', label='Upper Band')
ax.plot(df['timestamp'], df['lower_band'], color='black', label='Lower Band')

ax2 = ax.twinx()
ax2.bar(df['timestamp'], df['price'], color='r', alpha=0.5, width=0.2)
ax2.set_ylabel('Price (USD)', color='r')
ax2.tick_params('y', colors='r')
ax2.format_ydata = lambda x: f'${x:.2f}'
ax2.yaxis.set_major_formatter(FormatStrFormatter('$%.2f'))

unique_timestamps = df['timestamp'].unique()
tick_indices = [i for i, x in enumerate(df['timestamp']) if x in unique_timestamps]

num_ticks = 5
tick_step = max(1, len(tick_indices) // (num_ticks - 1))
tick_indices = tick_indices[::tick_step]

ax.set_xticks(df['timestamp'].iloc[tick_indices])
ax.set_xticklabels(df['timestamp'].iloc[tick_indices], rotation=45)

ax.set_xlabel('Time')
ax.set_ylabel('exchange balance')

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.suptitle('Bitcoin Price with Bollinger Bands')
plt.savefig(coin + '_bollinger_bands_testing.png', dpi=300)
plt.show()
