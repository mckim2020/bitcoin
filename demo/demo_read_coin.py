import os, sys
import time
sys.path.extend([os.path.abspath('../python')])
from coin_master import Reader, Visualizer, Simulator


config = {'current_url': "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
          'history_url': "https://api.exchange.coinbase.com/products/BTC-USD/candles",
          'days': 30,
          'granularity': 86400
         }
read_config = None

reader = Reader(config, read_config)
visualizer = Visualizer(config)
simulator = Simulator(reader=reader, visualizer=visualizer, config=config, trader=None)

price_list = []
volume_list = []

for itr in range(100):
    price = simulator.reader.get_current_price()
    volume = simulator.reader.get_current_volume()
    price_list.append(price)
    volume_list.append(volume)
    time.sleep(1)
    print(f"Iteration {itr+1}/100 - "
          f"Price: ${price:,.2f}, "
          f"Volume: {volume:,.2f} BTC")

simulator.visualizer.plot_prices(price_list, fig_path="price_plot.png")
simulator.visualizer.plot_volumes(volume_list, fig_path="volume_plot.png")