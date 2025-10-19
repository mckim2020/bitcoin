import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, config):
        self.config = config
        self.set_mpl_params()


    def set_mpl_params(self):
        plt.rcParams['font.size'] = 18             # General font size
        plt.rcParams['axes.labelsize'] = 20        # Font size for x and y labels
        plt.rcParams['axes.titlesize'] = 20        # Font size for the plot title
        plt.rcParams['xtick.labelsize'] = 20       # Font size for x-axis ticks
        plt.rcParams['ytick.labelsize'] = 20       # Font size for y-axis ticks
        plt.rcParams['legend.fontsize'] = 20       # Font size for the legend
        plt.rcParams['axes.linewidth'] = 1.2       # Line width for the axes
        plt.rcParams['image.cmap'] = 'RdBu'        # 'RdBu' or 'jet' # or 'coolwarm'

        if self.config['use_tex']:
            plt.rcParams["text.usetex"] = True
            plt.rcParams["font.family"] = "serif"
            plt.rcParams["font.serif"] = ["Computer Modern Roman"]


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


    def plot_prices_with_predictions(self, price_list, pred_list, sigma=None, fig_path=None):
        """Plot price data with predictions"""
        plt.figure(figsize=(10, 10))
        plt.plot(range(len(price_list)), price_list, 
                 marker='*', linestyle='-', 
                 label='Historical Prices', color='black',
                 markersize=8, linewidth=1)
        plt.plot(range(len(pred_list)), pred_list, 
                 label='Predicted Prices',
                 color='red')
        if sigma is not None:
            plt.fill_between(range(len(pred_list)), 
                             pred_list.flatten() - 1.96*sigma, 
                             pred_list.flatten() + 1.96*sigma, 
                             color='gray', alpha=0.2, label='95% Confidence Interval')
        plt.xlabel('Time Step')
        plt.ylabel('Normalized Price')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        if fig_path:
            plt.savefig(fig_path, dpi=300)
        else:
            plt.show()
        plt.close()