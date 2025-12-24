import math
import numpy as np

class NelsonSiegelCurveModel:
    def __init__(self, beta0, beta1, beta2, tau):
        self.beta0 = beta0
        self.beta1 = beta1
        self.beta2 = beta2
        self.tau = tau

    def df(self, t):
        # Linear interpolation between 0 and 0.25
        if t <= 0.25:
            t_knot = 0.25
            power_term = self.beta0 * t_knot + (self.beta1 + self.beta2) * (1 - math.exp(-t_knot / self.tau) * self.tau) - self.beta2 * t_knot * math.exp(-t_knot / self.tau)
            df_knot = math.exp(-power_term)
            df_0 = 1

            df = df_0 + (t / t_knot) * (df_knot - df_0)
        else:
            power_term = self.beta0 * t + (self.beta1 + self.beta2) * (1 - math.exp(-t / self.tau) * self.tau) - self.beta2 * t * math.exp(-t / self.tau)

            df = math.exp(-power_term)

        return df

    def zero_rate(self, t):
        return -np.log(self.df(t) / t)

    def forward_rate(self, t1, t2):
        return (self.df(t1) / self.df(t2) - 1) / (t2 - t1)