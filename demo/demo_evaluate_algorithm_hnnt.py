import os, sys
import tqdm
import torch
import numpy as np
sys.path.extend([os.path.abspath('../python')])
from coin_master import Reader, Regressor, Trader, Visualizer, Simulator
from coin_master.models.models import TanhMLP, GELUMLP, SILUMLP


config = {'current_url': "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
          'history_csv': "./data/btcusd_1-min_data.csv",
          'torch_dtype': torch.float32,
          'device': torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
          'verbose': True,
          'use_tex': False}
read_config = {'start_step': 6000000,
               'history': None}
trade_config = {'algorithm': 'hnnt',
                'stride': 1000,
                'step_size': 1,
                'window_size': 100,
                'n_epochs': 1000}
wallet = []
model=GELUMLP(hidden_size=64)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

reader = Reader(config, read_config)
regressor = Regressor(config, model=model, optimizer=optimizer)
trader = Trader(config, trade_config, wallet, reader, regressor)
visualizer = Visualizer(config)
simulator = Simulator(reader=reader, visualizer=visualizer, config=config, trader=trader)

simulator.trader.reader.step = 0
simulator.trader.wallet = []
read_config['start_step'] = np.random.randint(6000000, 7000000, 1)
norm_prices, pred_prices = simulator.trader.hnnt_demo(demo_steps=100, mean_every=1, n_epochs=1000)
simulator.visualizer.plot_prices_with_predictions(norm_prices, pred_prices)
raise ValueError("Stop here")

n_tests = 1
profits = []

for _ in tqdm.tqdm(range(n_tests)):
    simulator.trader.reader.step = 0
    simulator.trader.wallet = []
    read_config['start_step'] = np.random.randint(6000000, 7000000, 1)
    simulator.trader.trade()
    total_usd, _total_vol = simulator.trader.evaluate_wallet()
    profits.append(total_usd)

print(f"Average profit over {n_tests} tests: ${np.mean(profits):,.2f} ± ${np.std(profits):,.2f}")