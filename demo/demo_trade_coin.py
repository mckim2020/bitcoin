import os, sys
import time
sys.path.extend([os.path.abspath('../python')])
from coin_master import Reader, Trader, Visualizer, Simulator


config = {'current_url': "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
          'time_step_size': 1.0,
          'short_window': 5,
          'long_window': 20,
          'verbose': True}
wallet = []

reader = Reader(config)
trader = Trader(config, wallet, reader)
visualizer = Visualizer(config)
simulator = Simulator(reader=reader, visualizer=visualizer, config=config, trader=trader)

simulator.trader.mean_value_trading()
total_usd, total_vol = simulator.trader.evaluate_wallet()
print(f"Final Wallet Evaluation: USD: ${total_usd:,.2f}, BTC: {total_vol:.4f}")