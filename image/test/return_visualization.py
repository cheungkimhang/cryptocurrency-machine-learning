import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

coin = "bTC"
df = pd.read_csv(r"image\result\bt_exchange_balance_BTC_binance_delay_0_testing.csv")
num_rows = len(df)
keep_rows = list(range(0, num_rows, 144))
df = df.iloc[keep_rows]

fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(df['timestamp'], df['cumulative earnings $'], color='red', label='strategy cumulative earnings')
ax.plot(df['timestamp'], df['control_experiment'], color='black', label='long holding ' + coin)

unique_timestamps = df['timestamp'].unique()
tick_indices = [i for i, x in enumerate(df['timestamp']) if x in unique_timestamps]

num_ticks = 5
tick_step = max(1, len(tick_indices) // (num_ticks - 1))
tick_indices = tick_indices[::tick_step]

ax.set_xticks(df['timestamp'].iloc[tick_indices])
ax.set_xticklabels(df['timestamp'].iloc[tick_indices], rotation=45)

ax.set_xlabel('Time')

ax.set_ylabel('Earnings ($)')

plt.title('Cumulative Earnings Comparison')

ax.legend()

plt.show()