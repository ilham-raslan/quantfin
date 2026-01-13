import numpy as np

from quantfin.vol.vol_calibrator import VolCalibrator

class VolSurface:
    """Represents a volatility surface: vol = f(strike, expiry)"""

    def __init__(self, expiries=None, strikes=None, vols=None, forwards=None):
        self.expiries = expiries if expiries is not None else []
        self.strikes = strikes if strikes is not None else []
        self.vols = vols if vols is not None else []
        self.forwards = forwards if forwards is not None else []
        self.models = {}

    def add_market_vol(self, expiry, strike, vol, forward):
        self.expiries.append(expiry)
        self.strikes.append(strike)
        self.vols.append(vol)
        self.forwards.append(forward)

    def calibrate(self, engine="scipy"):
        expiry_to_indices = {}

        for i, T in enumerate(self.expiries):
            if T not in expiry_to_indices:
                expiry_to_indices[T] = [i]
            else:
                expiry_to_indices[T].append(i)

        for expiry, indices in expiry_to_indices.items():
            expiries = [self.expiries[i] for i in indices]
            strikes = [self.strikes[i] for i in indices]
            vols = [self.vols[i] for i in indices]
            forwards = [self.forwards[i] for i in indices]
            calibrator = VolCalibrator(expiries, strikes, vols, forwards)
            self.models[expiry] = calibrator.calibrate(engine=engine)

    def get_vol(self, expiry, strike, forward):
        """Return interpolated vol for a given expiry/strike"""
        if not self.models:
            raise Exception("Model is not yet calibrated, run calibrate() first")

        i, point = 0, 0
        expiries = list(self.models.keys())
        for i, point in enumerate(expiries):
            if expiry == point:
                return self.models[point].get_vol(expiry, strike, forward)
            elif expiry > point:
                continue
            else:
                break

        left_vol = self.models[expiries[i - 1]].get_vol(expiry, strike, forward)
        right_vol = self.models[expiries[i]].get_vol(expiry, strike, forward)

        return left_vol + ((right_vol - left_vol) / (expiries[i] - expiries[i - 1])) * (expiry - expiries[i - 1])
