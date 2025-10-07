import os, sys
import tqdm
import numpy as np
sys.path.extend([os.path.abspath('../python')])
from coin_master import Reader, Trader, Visualizer, Simulator


config = {'current_url': "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
          'history_csv': "./data/btcusd_1-min_data.csv",
          'verbose': False}
read_config = {'start_step': 6000000,
               'history': None}
trade_config = {'algorithm': 'hhhmvt',
                'stride': 1000,
                'step_size': 1,
                'window_1': 256,
                'window_2': 64,
                'window_3': 16}
wallet = []

reader = Reader(config, read_config)
trader = Trader(config, trade_config, wallet, reader)
simulator = Simulator(reader=reader, visualizer=None, config=config, trader=trader)

n_tests = 1000
profits = []

for _ in tqdm.tqdm(range(n_tests)):
    simulator.trader.reader.step = 0
    simulator.trader.wallet = []
    read_config['start_step'] = np.random.randint(6000000, 7000000, 1)
    simulator.trader.trade()
    total_usd, _total_vol = simulator.trader.evaluate_wallet()
    profits.append(total_usd)

print(f"Average profit over {n_tests} tests: ${np.mean(profits):,.2f} ± ${np.std(profits):,.2f}")