import os, sys
import time
sys.path.extend([os.path.abspath('../python')])
from coin_master import Reader, Trader, Visualizer, Simulator


config = {'current_url': "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
          'history_csv': "./data/btcusd_1-min_data.csv",
          'start': 7000000,
          'verbose': True}
read_config = {'start_step': 6000000,
               'history': None}
trade_config = {'algorithm': 'hmvt',
                'stride': 100,
                'step_size': 1,
                'short_window': 5,
                'long_window': 10}
wallet = []

reader = Reader(config, read_config)
trader = Trader(config, trade_config, wallet, reader)
visualizer = Visualizer(config)
simulator = Simulator(reader=reader, visualizer=visualizer, config=config, trader=trader)

simulator.trader.trade()
simulator.trader.evaluate_algorithm()