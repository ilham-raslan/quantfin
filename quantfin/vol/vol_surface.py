from quantfin.vol.vol_calibrator import VolCalibrator

class VolSurface:
    """Represents a volatility surface: vol = f(strike, expiry)"""

    def __init__(self, expiries=None, strikes=None, vols=None, forwards=None):
        self.expiries = expiries if expiries is not None else []
        self.strikes = strikes if strikes is not None else []
        self.vols = vols if vols is not None else []
        self.forwards = forwards if forwards is not None else []
        self.model = None

    def add_market_vol(self, expiry, strike, vol, forward):
        self.expiries.append(expiry)
        self.strikes.append(strike)
        self.vols.append(vol)
        self.forwards.append(forward)

    def calibrate(self):
        calibrator = VolCalibrator(self.expiries, self.strikes, self.vols, self.forwards)
        self.model = calibrator.calibrate()

    def get_vol(self, expiry, strike, forward):
        """Return interpolated vol for a given expiry/strike"""
        if self.model is not None:
            return self.model.get_vol(expiry, strike, forward)
        else:
            raise Exception("Model is not yet calibrated, run calibrate() first")
