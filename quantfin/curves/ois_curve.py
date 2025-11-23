import math
import matplotlib.pyplot as plt
import numpy as np

from quantfin.bootstrap.interpolation import LogLinearInterpolator

class OISCurve:
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
        return -1 * math.log(self.df(t)) / t

    def plot_dfs(self, t_start=None, t_end=None):
        t_start = t_start if t_start is not None else 0
        t_end = t_end if t_end is not None else self.times[-1]
        intervals = int((t_end - t_start) * 10)

        tenors = np.linspace(t_start, t_end, intervals)
        dfs = [self.df(t) for t in tenors]

        plt.plot(tenors, dfs, marker=".")
        plt.title("Discount Factors")
        plt.xlabel("Tenor (years)")
        plt.ylabel("DF")
        plt.grid(True)
        plt.show()

    def plot_zero_rates(self, t_start=None, t_end=None):
        t_start = t_start if t_start is not None else 0
        t_end = t_end if t_end is not None else self.times[-1]
        intervals = int((t_end - t_start) * 10)

        tenors = np.linspace(t_start, t_end, intervals)
        # bump 0 point with epsilon given divide by 0 error
        if tenors[0] == 0:
            tenors[0] = tenors[0] + 1e-8

        zero_rates = [self.zero_rate(t) for t in tenors]

        plt.plot(tenors, zero_rates, marker=".")
        plt.title("Zero Rates")
        plt.xlabel("Tenor (years)")
        plt.ylabel("r")
        plt.grid(True)
        plt.show()
