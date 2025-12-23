import numpy as np

class Curve:
    def __init__(self, df_provider):
        self.df_provider = df_provider

    def df(self, t):
        return self.df_provider.df(t)

    def zero_rate(self, t):
        return -np.log(self.df(t)) / t

    def forward_rate(self, t1, t2):
        return (self.df(t1) / self.df(t2) - 1) / (t2 - t1)