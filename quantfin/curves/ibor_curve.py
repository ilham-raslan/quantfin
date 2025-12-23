import matplotlib.pyplot as plt
import numpy as np

from quantfin.bootstrap.interpolation import LogLinearInterpolator


class IBORCurve3M:
    def __init__(self, ois_curve):
        self.times = [0]
        self.dfs = [1]

    def add_knot(self, t, df):
        self.times.append(t)
        self.dfs.append(df)

    def df(self, t):
        interpolator = LogLinearInterpolator(self.times, self.dfs)
        return interpolator(t)

    def forward_rate(self, t1, t2):
        return (self.df(t1) / self.df(t2) - 1) / 0.25

    def plot_forward_rates(self, t_start=None, t_end=None):
        t_start = t_start if t_start is not None else 0
        t_end = t_end if t_end is not None else self.times[-2]
        intervals = int((t_end - t_start) * 10)

        tenors = np.linspace(t_start, t_end, intervals)
        # bump 0 point with epsilon given divide by 0 error
        # if tenors[0] == 0:
        #     tenors[0] = tenors[0] + 1e-8

        forward_rates = [self.forward_rate(t, t + 0.25) for t in tenors]

        plt.plot(tenors, forward_rates, marker=".")
        plt.title("Forward Rates")
        plt.xlabel("Tenor (years)")
        plt.ylabel("r")
        plt.grid(True)
        plt.show()
