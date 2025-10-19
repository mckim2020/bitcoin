import torch
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, ExpSineSquared, WhiteKernel, DotProduct, Matern, RationalQuadratic


class Regressor:
    def __init__(self, config, model=None, optimizer=None):
        self.config = config
        self.model = model
        self.optimizer = optimizer
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


    def train_gpr(self, X_train, y_train):
        """Train the Gaussian Process Regressor"""
        self.gp.fit(X_train, y_train)


    def predict_gpr(self, X_test):
        """Predict using the trained Gaussian Process Regressor"""
        y_pred, sigma = self.gp.predict(X_test, return_std=True)
        return y_pred, sigma


    def train_nn(self, X_train, y_train, n_epochs=1000):
        """Train the Neural Network Regressor"""
        X_train = torch.tensor(X_train, dtype=self.config['torch_dtype'], device=self.config['device'])
        y_train = torch.tensor(y_train, dtype=self.config['torch_dtype'], device=self.config['device'])

        for epoch in range(n_epochs):
            self.model.train()
            self.optimizer.zero_grad()
            y_pred = self.model(X_train)
            loss = torch.nn.functional.mse_loss(y_pred, y_train)
            loss.backward()
            self.optimizer.step()
        y_pred = self.model(X_train)
        return y_pred


    def predict_nn(self, X_test):
        """Predict using the trained Neural Network Regressor"""
        X_test = torch.tensor(X_test, dtype=self.config['torch_dtype'], device=self.config['device'])
        return self.model(X_test).detach().cpu().numpy().flatten()