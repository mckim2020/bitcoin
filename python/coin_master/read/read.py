import requests
import json
import time
import numpy as np
from datetime import datetime, timedelta


class Reader:
    def __init__(self, config, read_config):
        self.config = config
        self.read_config = read_config
        self.step = 0


    def get_current_ticker(self):
        """Get detailed Bitcoin ticker from Coinbase Pro API"""
        try:
            response = requests.get(self.config['current_url'])
            response.raise_for_status()
            data = response.json()
            
            # print(f"Bitcoin (BTC-USD) Ticker:")
            # print(f"Price: ${float(data['price']):,.2f}")
            # print(f"24h Volume: {float(data['volume']):,.2f} BTC")
            # print(f"Best Bid: ${float(data['bid']):,.2f}")
            # print(f"Best Ask: ${float(data['ask']):,.2f}")

            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None


    def get_current_price(self):
        coin_data = self.get_current_ticker()
        return float(coin_data['price']) if coin_data else None


    def get_current_volume(self):
        coin_data = self.get_current_ticker()
        return float(coin_data['volume']) if coin_data else None


    def get_history_price(self):
        if self.read_config['history'] is None:
            self.read_config['history'] = np.loadtxt(self.config['history_csv'], delimiter=',', skiprows=1)
        return self.read_config['history'][self.read_config['start_step'] + self.step, 4][0] # close prices


    def get_history_volume(self):
        if self.read_config['history'] is None:
            self.read_config['history'] = np.loadtxt(self.config['history_csv'], delimiter=',', skiprows=1)
        return self.read_config['history'][self.read_config['start_step'] + self.step, 5][0] # volume


    def read_coin_data(self, time_step_size=1.0, n_steps=100, json_path=None):
        price_list = []
        volume_list = []

        for itr in range(n_steps):
            current_coin_data = self.get_current_ticker()
            price_list.append(float(current_coin_data['price']))
            volume_list.append(float(current_coin_data['volume']))
            time.sleep(time_step_size)
            print(f"Iteration {itr+1}/{n_steps} - "
                f"Price: ${float(current_coin_data['price']):,.2f}, "
                f"Volume: {float(current_coin_data['volume']):,.2f} BTC")

        return price_list, volume_list


    # def get_historical_ticker(self):
    #     """
    #     Get historical ticker data (OHLCV) from Coinbase Pro API
        
    #     Parameters
    #     ----------
    #     symbol: Trading pair (e.g., "BTC-USD", "ETH-USD")
    #     days: Number of days of historical data
    #     granularity: Time interval in seconds
    #     """
    #     try:
    #         end_time = datetime.now()
    #         start_time = end_time - timedelta(days=self.config['days'])
            
    #         start_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    #         end_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
    #         params = {
    #             'start': start_str,
    #             'end': end_str,
    #             'granularity': self.config['granularity']
    #         }
            
    #         response = requests.get(self.config['history_url'], params=params)
    #         response.raise_for_status()
    #         data = response.json()

    #         ticker_data = []
    #         for candle in reversed(data):  # Reverse to get chronological order
    #             ticker_info = {
    #                 'timestamp': datetime.fromtimestamp(candle[0]),
    #                 'low': candle[1],
    #                 'high': candle[2],
    #                 'open': candle[3],
    #                 'close': candle[4],
    #                 'volume': candle[5]
    #             }
    #             ticker_data.append(ticker_info)
            
    #         return ticker_data
            
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error fetching historical ticker: {e}")
    #         return None