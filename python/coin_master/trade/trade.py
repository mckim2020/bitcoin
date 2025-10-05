import numpy as np
import time


class Trader:
    def __init__(self, config, wallet, reader):
        self.config = config
        self.wallet = wallet
        self.reader = reader


    def evaluate_wallet(self):
        """Evaluate the current state of the wallet"""
        total_usd = 0.0
        total_vol = 0.0

        for transaction in self.wallet:
            if transaction['action'] == 'buy':
                total_usd -= transaction['usd'] * transaction['vol']
                total_vol += transaction['vol']

            elif transaction['action'] == 'sell':
                total_usd += transaction['usd'] * transaction['vol']
                total_vol -= transaction['vol']

            else:
                raise ValueError("Unknown transaction action")

        return total_usd, total_vol


    def buy(self, price, volume):
        """Simulate a buy action"""
        self.wallet.append({'usd': price, 'vol': volume, 'action': 'buy'})

        if self.config['verbose']:
            print(f"Buying {volume:.4f} BTC at ${price:,.2f} each.")


    def sell(self, price, volume):
        """Simulate a sell action"""
        self.wallet.append({'usd': price, 'vol': volume, 'action': 'sell'})

        if self.config['verbose']:
            print(f"Selling {volume:.4f} BTC at ${price:,.2f} each.")


    def mean_value_trading(self):
        price_history = []

        while True:
            price = self.reader.get_current_price()
            price_history.append(price)

            if len(price_history) > self.config['long_window']:
                short_avg = np.mean(price_history[-self.config['short_window']:])
                long_avg = np.mean(price_history[-self.config['long_window']:])

                if short_avg > long_avg:
                    self.buy(price, 0.01) # buy 0.01 BTC

                elif short_avg < long_avg:
                    self.sell(price, 0.01) # sell 0.01 BTC

            time.sleep(self.config['time_step_size'])
