import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, ExpSineSquared, WhiteKernel, DotProduct, Matern, RationalQuadratic


class Regressor:
    def __init__(self, config):
        self.config = config
        kernel = (
            # Long-term trend - much wider bounds
            C(1.0, (1e-10, 1e10)) * DotProduct(sigma_0=1.0, sigma_0_bounds=(1e-10, 1e10)) +
            
            # # Periodic component - much wider bounds
            # C(1.0, (1e-10, 1e10)) * ExpSineSquared(
            #     length_scale=1.0, 
            #     periodicity=1.0,
            #     length_scale_bounds=(1e-10, 1e10),
            #     periodicity_bounds=(1e-3, 1e6)  # Much wider periodicity bounds
            # ) +
            
            # Local variations - much wider bounds
            C(1.0, (1e-10, 1e10)) * RBF(length_scale=1.0, length_scale_bounds=(1e-10, 1e10))
            
            # # White noise - much wider bounds
            # WhiteKernel(noise_level=1e-9, noise_level_bounds=(1e-15, 1e0))
        )
        self.gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)


    def train(self, X_train, y_train):
        """Train the Gaussian Process Regressor"""
        self.gp.fit(X_train, y_train)


    def predict(self, X_test):
        """Predict using the trained Gaussian Process Regressor"""
        y_pred, sigma = self.gp.predict(X_test, return_std=True)
        return y_pred, sigma