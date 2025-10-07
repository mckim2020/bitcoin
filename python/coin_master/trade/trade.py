import numpy as np
import time


class Trader:
    def __init__(self, config, trade_config, wallet, reader):
        self.config = config
        self.trade_config = trade_config
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


    def evaluate_algorithm(self):
        """Evaluate the trading algorithm performance"""
        total_usd, total_vol = self.evaluate_wallet()
        current_price = self.reader.get_current_price()
        total_value = total_usd + (total_vol * current_price)

        if self.config['verbose']:
            print(f"Wallet Evaluation: USD: ${total_usd:,.2f}, BTC: {total_vol:.4f}, "
                  f"Total Value: ${total_value:,.2f} at Current Price: ${current_price:,.2f}")

        return total_value


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


    def rmvt(self):
        """ Real-time Mean Value Trading Algorithm """
        price_history = []

        for itr in range(self.trade_config['stride']):
            price = self.reader.get_current_price()
            price_history.append(price)

            if len(price_history) > self.trade_config['long_window']:
                _total_usd, total_vol = self.evaluate_wallet()

                short_avg = np.mean(price_history[-self.trade_config['short_window']:])
                long_avg = np.mean(price_history[-self.trade_config['long_window']:])

                if short_avg > long_avg:
                    self.buy(price, 0.01) # buy 0.01 BTC

                elif short_avg < long_avg and total_vol > 0:
                    self.sell(price, 0.01) # sell 0.01 BTC

            time.sleep(self.trade_config['time_step_size'])

            if self.config['verbose']:
                print(f"[{itr}/{self.trade_config['stride']}] Current Price: ${price:,.2f}")
        
        total_usd, total_vol = self.evaluate_wallet()
        self.sell(self.reader.get_current_price(), total_vol) # sell all remaining BTC


    def hmvt(self):
        """ Historical Mean Value Trading Algorithm """
        price_history = []

        for itr in range(self.trade_config['stride']):
            price = self.reader.get_history_price()
            price_history.append(price)

            if len(price_history) > self.trade_config['long_window']:
                _total_usd, total_vol = self.evaluate_wallet()

                short_avg = np.mean(price_history[-self.trade_config['short_window']:])
                long_avg = np.mean(price_history[-self.trade_config['long_window']:])

                if short_avg > long_avg:
                    self.buy(price, 0.01) # buy 0.01 BTC

                elif short_avg < long_avg and total_vol > 0:
                    self.sell(price, 0.01) # sell 0.01 BTC

            self.reader.step += self.trade_config['step_size']

            if self.config['verbose']:
                print(f"[{itr}/{self.trade_config['stride']}] Current Price: ${price:,.2f}")
        
        total_usd, total_vol = self.evaluate_wallet()
        self.sell(self.reader.get_history_price(), total_vol) # sell all remaining BTC


    def trade(self):
        if self.trade_config['algorithm'] == 'rmvt':
            self.rmvt()
        elif self.trade_config['algorithm'] == 'hmvt':
            self.hmvt()
        else:
            raise ValueError("Unknown trading algorithm")