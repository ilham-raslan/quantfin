from quantfin.bootstrap.interpolation import LogLinearInterpolator
import numpy as np

class LogLinearBootstrappedCurveModel:
    def __init__(self):
        self.times = [0]
        self.dfs = [1]

    def add_knot(self, t, df):
        self.times.append(t)
        self.dfs.append(df)

    def df(self, t):
        interpolator = LogLinearInterpolator(self.times, self.dfs)
        return interpolator(t)

    def zero_rate(self, t):
        return -np.log(self.df(t)) / t

    def forward_rate(self, t1, t2):
        return (self.df(t1) / self.df(t2) - 1) / (t2 - t1)
