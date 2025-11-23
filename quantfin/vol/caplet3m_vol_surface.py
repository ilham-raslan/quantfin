from quantfin.vol.caplet3m_vol_calibrator import Caplet3MVolCalibrator
import numpy as np
import matplotlib.pyplot as plt

class Caplet3MVolSurface:
    """Represents a volatility surface for 3m caplets: vol = f(strike, expiry)"""

    def __init__(self, caplets = None, ibor_curve = None):
        self.caplets = caplets if caplets is not None else []
        self.ibor_curve = ibor_curve
        self.model = None

    def add_caplet(self, caplet):
        self.caplets.append(caplet)

    def calibrate(self):
        calibrator = Caplet3MVolCalibrator(self.caplets, self.ibor_curve)
        self.model = calibrator.calibrate()

    def get_vol(self, expiry, strike, forward):
        """Return interpolated vol for a given expiry/strike"""
        if self.model is not None:
            return self.model.get_vol(expiry, strike, forward)
        else:
            raise Exception("Model is not yet calibrated, run calibrate() first")

    def plot_calibrated_vol_surface(self, expiry_start, expiry_end, strike_start, strike_end):
        if self.model is None:
            raise Exception("Model is not yet calibrated, run calibrate() first")

        expiry_intervals = 100
        expiries = np.linspace(expiry_start, expiry_end, expiry_intervals)

        strike_intervals = 100
        strikes = np.linspace(strike_start, strike_end, strike_intervals)

        x, y = np.meshgrid(expiries, strikes, indexing="ij")
        z = np.zeros((len(expiries), len(strikes)))

        for i, t in enumerate(expiries):
            for j, k in enumerate(strikes):
                f = self.ibor_curve.forward_rate(t, t + 0.25)
                z[i, j] = self.get_vol(t, k, f)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap="viridis")
        ax.set_xlabel("Expiry (years)")
        ax.set_ylabel("Strike")
        ax.set_zlabel("Volatility")
        ax.set_title("Volatility Surface")

        plt.show()
