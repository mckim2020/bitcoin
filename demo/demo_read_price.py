import os, sys
import time
sys.path.extend([os.path.abspath('../python')])
from coin_master import Reader, Visualizer, Simulator


config = {'current_url': "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
          'history_url': "https://api.exchange.coinbase.com/products/BTC-USD/candles",
          'days': 30,
          'granularity': 86400
         }

reader = Reader(config)
visualizer = Visualizer(config)
simulator = Simulator(reader=reader, visualizer=visualizer, config=config, trader=None)

current_coin_data = simulator.reader.get_current_ticker()
historical_coin_data = simulator.reader.get_historical_ticker()

price_list = []
volume_list = []

for itr in range(100):
    current_coin_data = simulator.reader.get_current_ticker()
    price_list.append(float(current_coin_data['price']))
    volume_list.append(float(current_coin_data['volume']))
    time.sleep(1)
    print(f"Iteration {itr+1}/100 - "
          f"Price: ${float(current_coin_data['price']):,.2f}, "
          f"Volume: {float(current_coin_data['volume']):,.2f} BTC")

simulator.visualizer.plot_prices(price_list, fig_path="price_plot.png")
simulator.visualizer.plot_volumes(volume_list, fig_path="volume_plot.png")