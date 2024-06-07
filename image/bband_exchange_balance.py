import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def SMA():
    return True

try:
    BTC = pd.read_csv(r"image/raw_data/BTC.csv")

    EB = pd.DataFrame()
    EB["timestamp"] = BTC["timestamp"]
    EB["price"] = BTC["price_usd_close"]
    EB["exchange_balance"] = BTC["exchange_balance"]

    EB = EB.dropna()

    df = EB.copy()

    N = 2880

    df['SMA'] = df['exchange_balance'].rolling(window=N).mean()
    df['std'] = df['exchange_balance'].rolling(window=N).std()
    df['upper_band'] = df['SMA'] + 2 * df['std']
    df['lower_band'] = df['SMA'] - 2 * df['std']

    df = df.iloc[N-1:]

    print(df)

    df = df[100000::100]

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

except Exception as e:
    print(f"An error occurred: {e}")