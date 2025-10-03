import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, config):
        self.config = config


    def plot_prices(self, price_list, fig_path=None):
        """Plot price data"""
        plt.figure(figsize=(10, 5))
        plt.plot(price_list, label='Price', color='blue')
        plt.title('Bitcoin Price Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)
        if fig_path:
            plt.savefig(fig_path, dpi=300)
        else:
            plt.show()
        plt.close()


    def plot_volumes(self, volume_list, fig_path=None):
        """Plot volume data"""
        plt.figure(figsize=(10, 5))
        plt.plot(volume_list, label='Volume', color='orange')
        plt.title('Bitcoin Volume Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Volume (BTC)')
        plt.legend()
        plt.grid(True)
        if fig_path:
            plt.savefig(fig_path, dpi=300)
        else:
            plt.show()
        plt.close()