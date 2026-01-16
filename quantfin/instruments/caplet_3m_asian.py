import math
import random

from scipy.stats import norm


class Caplet3MAsian:
    def __init__(self, expiry, strike, notional=1, market_vol=None):
        self.expiry = expiry
        self.strike = strike
        self.notional = notional
        self.market_vol = market_vol
        self.accrual = 0.25

    def forward_rate(self, ibor_curve):
        return ibor_curve.forward_rate(self.expiry, self.expiry + self.accrual)

    def price(self, ois_curve, ibor_curve, vol_surface, iterations=1000, increment=0.01):
        # We do monte carlo simulations to find the average 3m forward rate, then use that in the payoff
        notional = self.notional
        expiry = self.expiry
        strike = self.strike
        forward = self.forward_rate(ibor_curve)

        sigma = vol_surface.get_vol(expiry, strike, forward)
        df = ois_curve.df(expiry)

        C_list = []

        for i in range(iterations):
            F_list = []
            F_list.append(forward)
            timesteps = int(expiry / increment)

            for j in range(timesteps):
                z = random.gauss(0, 1)
                # here we use truncation at 0
                F_pos = max(F_list[-1] + sigma * (math.sqrt(F_list[-1])) * math.sqrt(increment) * z, 0)
                F_list.append(F_pos)

            F = sum(F_list) / timesteps
            C = notional * df * max(F - strike, 0)
            C_list.append(C)

        return sum(C_list) / iterations
