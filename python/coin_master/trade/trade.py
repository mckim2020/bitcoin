import numpy as np
import time


class Trader:
    def __init__(self, config, trade_config, wallet, reader, regressor=None):
        self.config = config
        self.trade_config = trade_config
        self.wallet = wallet
        self.reader = reader
        self.regressor = regressor


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
            print(f"\nBuying {volume:.4f} BTC at ${price:,.2f} each.\n")


    def sell(self, price, volume):
        """Simulate a sell action"""
        self.wallet.append({'usd': price, 'vol': volume, 'action': 'sell'})

        if self.config['verbose']:
            print(f"\nSelling {volume:.4f} BTC at ${price:,.2f} each.\n")


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


    def hhhmvt(self):
        """ Historical Mean Value Trading Algorithm """
        price_history = []

        for itr in range(self.trade_config['stride']):
            price = self.reader.get_history_price()
            price_history.append(price)

            if len(price_history) > self.trade_config['long_window']:
                _total_usd, total_vol = self.evaluate_wallet()

                avg_1 = np.mean(price_history[-self.trade_config['window_1']:])
                avg_2 = np.mean(price_history[-self.trade_config['window_2']:])
                avg_3 = np.mean(price_history[-self.trade_config['window_3']:])

                if short_avg > long_avg:
                    self.buy(price, 0.01) # buy 0.01 BTC

                elif short_avg < long_avg and total_vol > 0:
                    self.sell(price, 0.01) # sell 0.01 BTC

            self.reader.step += self.trade_config['step_size']

            if self.config['verbose']:
                print(f"[{itr}/{self.trade_config['stride']}] Current Price: ${price:,.2f}")
        
        total_usd, total_vol = self.evaluate_wallet()
        self.sell(self.reader.get_history_price(), total_vol) # sell all remaining BTC


    def hgprt_demo(self, demo_steps=1000, mean_every=10):
        import tqdm
        price_history = []
        assert demo_steps % mean_every == 0, "demo_steps must be divisible by mean_every"

        for itr in tqdm.tqdm(range(demo_steps)):
            price = self.reader.get_history_price()
            price_history.append(price)
            self.reader.step += self.trade_config['step_size']
        
        prices = np.array(price_history)
        prices = np.mean(prices.reshape(-1, mean_every), axis=1)
        norm_prices = (prices - np.mean(prices)) / np.std(prices)
        train_prices = norm_prices[:-int(len(norm_prices) * 0.1)]
        self.regressor.train(np.linspace(0.0, len(train_prices)-1, len(train_prices)).reshape(-1, 1), 
                             train_prices.reshape(-1, 1))
        pred_prices, sigma = self.regressor.predict(np.linspace(0.0, len(norm_prices)-1, len(norm_prices)).reshape(-1, 1))

        return norm_prices, pred_prices, sigma


    def hgprt(self):
        """ Historical Gaussian Process Regression Trading Algorithm """
        price_history = []

        for itr in range(self.trade_config['stride']):
            price = self.reader.get_history_price()
            price_history.append(price)

            if len(price_history) > self.trade_config['window_size']:
                _total_usd, total_vol = self.evaluate_wallet()

                prices = np.array(price_history[-self.trade_config['window_size']:])
                norm_prices = (prices - np.mean(prices)) / np.std(prices)
                self.regressor.train(np.linspace(0.0, len(prices)-1, len(prices)).reshape(-1, 1), 
                                     norm_prices.reshape(-1, 1))
                norm_prices_pred, _sigma = self.regressor.predict(np.linspace(0.0, len(prices)+9, len(prices)+10).reshape(-1, 1))
                norm_prices_future = norm_prices_pred[-10:]

                if np.mean(norm_prices_future) > norm_prices[-1]:
                    self.buy(price, 0.01) # buy 0.01 BTC

                elif np.mean(norm_prices_future) < norm_prices[-1] and total_vol > 0:
                    self.sell(price, 0.01) # sell 0.01 BTC

            self.reader.step += self.trade_config['step_size']

            if self.config['verbose']:
                print(f"[{itr}/{self.trade_config['stride']}] Current Price: ${price:,.2f}")
        
        total_usd, total_vol = self.evaluate_wallet()
        self.sell(self.reader.get_history_price(), total_vol) # sell all remaining BTC


    def hnnt(self):
        """ Historical Neural Network Trading Algorithm """
        pass


    def trade(self):
        if self.trade_config['algorithm'] == 'rmvt':
            self.rmvt()
        elif self.trade_config['algorithm'] == 'hmvt':
            self.hmvt()
        elif self.trade_config['algorithm'] == 'hhhmvt':
            self.hhhmvt()
        elif self.trade_config['algorithm'] == 'hgprt':
            self.hgprt()
        elif self.trade_config['algorithm'] == 'hnnt':
            self.hnnt()
        else:
            raise ValueError("Unknown trading algorithm")