import math
import numpy as np

from scipy.stats import norm


class Swaption3M:
    def __init__(self, expiry, strike, tenor, notional=1, market_vol=None):
        self.expiry = expiry
        self.strike = strike
        self.tenor = tenor
        self.notional = notional
        self.market_vol = market_vol
        self.accrual = 0.25

    def forward_swap_rate(self, ois_curve, ibor_curve):
        schedule = np.arange(self.expiry + self.accrual, self.expiry + self.tenor + 1e-12, self.accrual)
        denominator = sum(self.accrual * ois_curve.df(time) for time in schedule)
        numerator = sum(self.accrual * ibor_curve.forward_rate(time - self.accrual, time) * ois_curve.df(time) for time in schedule)
        return numerator / denominator

    def price(self, ois_curve, ibor_curve, vol_surface):
        expiry = self.expiry
        strike = self.strike
        tenor = self.tenor
        forward_swap_rate = self.forward_swap_rate(ois_curve, ibor_curve)
        accrual = self.accrual
        notional = self.notional

        schedule = np.arange(expiry + accrual, expiry + tenor + 1e-12, accrual)
        annuity = sum(accrual * ois_curve.df(time) for time in schedule)
        sigma = 0.2 # TODO: Actually build a swaption vol surface
        # sigma = vol_surface.get_vol(expiry, strike, forward)

        d_1 = (math.log(forward_swap_rate / strike) + (sigma ** 2) * expiry / 2) / (sigma * math.sqrt(expiry))
        d_2 = d_1 - sigma * math.sqrt(expiry)

        price = notional * annuity * (forward_swap_rate * norm.cdf(d_1) - strike * norm.cdf(d_2))

        return price
