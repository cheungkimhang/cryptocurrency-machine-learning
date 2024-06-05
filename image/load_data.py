import datetime
import pandas as pd
import requests

class get_data:
    def __init__(self):
        self.api_key_glassnode = "2RCN5Xk7lniklWmk09fVVmPq5L9"
        self.api_key_coinalyze = "ba93af56-e4e3-45af-bee7-0a6863f767ff"
    
    def get_long_short_ratio(self, symbols, endpoint_long_short_ratio, interval):
        asset = symbols + "USDT_PERP.A"
        frequency = interval
        endTime = datetime.datetime.now()
        startTime = endTime - datetime.timedelta(days=9999)
        startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")
        endTime = endTime.strftime("%Y-%m-%d %H:%M:%S")
        startTime = datetime.datetime.timestamp(
            datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        )
        endTime = datetime.datetime.timestamp(
            datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        )

        
        try:
            params = {
                "symbols": asset,
                "interval": frequency,
                "from": startTime,
                "to": endTime,
                "api_key": self.api_key_coinalyze,
            }

            response = requests.get(endpoint_long_short_ratio, params=params)
            empty_df = pd.DataFrame()
            data = response.json()
            data = pd.json_normalize(data, "history")
            data["t"] = pd.to_datetime(data["t"], unit="s").dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            data.rename(
                columns={"t": "timestamp", "r": "ratio", "l": "long", "s": "short"},
                inplace=True,
            )
            data = data[["timestamp", "ratio"]]
            
            return data
        except Exception as e:
            print(f"Error fetching BTCUSDT long-short ratio: {e}")
            return None
    
    def get_data_from_glassnode(self, symbols, endpoint, interval, exchange = "binance"):
        try:
            params = {
                "a": symbols,
                "f": "JSON",
                "i": interval,
                "e": exchange,
                "api_key": self.api_key_glassnode
                
            }

            response = requests.get(endpoint, params=params)
            data = response.json()
            data = pd.DataFrame(data)

            data.rename(
                columns={"t": "timestamp", "v": "value"},
                inplace=True,
            )
            data["timestamp"] = pd.to_datetime(data["timestamp"], unit="s").dt.strftime("%Y-%m-%d %H:%M:%S")

            return data
        
        except Exception as e:
            print(f"Error fetching data from {endpoint}: {e}")
            return None
