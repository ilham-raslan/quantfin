import numpy as np
import matplotlib.pyplot as plt

class Curve:
    def __init__(self, df_provider):
        self.df_provider = df_provider

    def df(self, t):
        return self.df_provider.df(t)

    def zero_rate(self, t):
        return self.df_provider.zero_rate(t)

    def forward_rate(self, t1, t2):
        return self.df_provider.forward_rate(t1, t2)

    def plot_dfs(self, t_start=None, t_end=None):
        t_start = t_start if t_start is not None else 0
        t_end = t_end if t_end is not None else self.df_provider.times[-1]
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
        t_end = t_end if t_end is not None else self.df_provider.times[-1]
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

    def plot_forward_rates(self, t_start=None, t_end=None):
        t_start = t_start if t_start is not None else 0
        t_end = t_end if t_end is not None else self.df_provider.times[-2]
        intervals = int((t_end - t_start) * 10)

        tenors = np.linspace(t_start, t_end, intervals)
        forward_rates = [self.forward_rate(t, t + 0.25) for t in tenors]

        plt.plot(tenors, forward_rates, marker=".")
        plt.title("Forward Rates")
        plt.xlabel("Tenor (years)")
        plt.ylabel("r")
        plt.grid(True)
        plt.show()

