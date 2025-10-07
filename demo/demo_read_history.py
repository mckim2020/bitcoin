import os, sys
import time
sys.path.extend([os.path.abspath('../python')])
from coin_master import Reader, Visualizer, Simulator


# https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data?resource=download
config = {'current_url': "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
          'history_csv': "./data/btcusd_1-min_data.csv",
          'verbose': True
         }
read_config = {'start_step': 7000000,
               'history': None
               }

reader = Reader(config, read_config)
visualizer = Visualizer(config)
simulator = Simulator(reader=reader, visualizer=visualizer, config=config, trader=None)

history_price = simulator.reader.get_history_price()
history_volume = simulator.reader.get_history_volume()
print(f"History Price: ${history_price:,.2f}, History Volume: {history_volume:,.2f} BTC")

price_list = []
volume_list = []

for itr in range(100):
    price = simulator.reader.get_history_price() # price
    volume = simulator.reader.get_history_volume() # volume
    price_list.append(price)
    volume_list.append(volume)
    simulator.reader.step += 1 # 1 minute step
    print(f"Iteration {itr+1}/100 - "
          f"Price: ${price:,.2f}, "
          f"Volume: {volume:,.2f} BTC")

simulator.visualizer.plot_prices(price_list, fig_path="price_plot.png")
simulator.visualizer.plot_volumes(volume_list, fig_path="volume_plot.png")