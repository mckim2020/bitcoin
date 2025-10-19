import torch
import torch.nn as nn
import torch.optim as optim


class TanhMLP(nn.Module):
    def __init__(self, hidden_size=64):
        super(TanhMLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(1, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1),
        )
    
    def forward(self, x):
        return self.layers(x)


class GELUMLP(nn.Module):
    def __init__(self, hidden_size=64):
        super(GELUMLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(1, hidden_size),
            nn.GELU(),
            nn.Linear(hidden_size, hidden_size),
            nn.GELU(),
            nn.Linear(hidden_size, hidden_size),
            nn.GELU(),
            nn.Linear(hidden_size, 1),
        )
    
    def forward(self, x):
        return self.layers(x)


class SILUMLP(nn.Module):
    def __init__(self, hidden_size=64):
        super(SILUMLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(1, hidden_size),
            nn.SiLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.SiLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.SiLU(),
            nn.Linear(hidden_size, 1),
        )
    
    def forward(self, x):
        return self.layers(x)