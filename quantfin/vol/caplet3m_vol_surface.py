import matplotlib.pyplot as plt
import numpy as np

from quantfin.vol.caplet3m_vol_calibrator import Caplet3MVolCalibrator


class Caplet3MVolSurface:
    """Represents a volatility surface for 3m caplets: vol = f(strike, expiry)"""

    def __init__(self, caplets = None, ibor_curve = None):
        self.caplets = caplets if caplets is not None else []
        self.ibor_curve = ibor_curve
        self.models = {}

    def add_caplet(self, caplet):
        self.caplets.append(caplet)

    def calibrate(self, engine="scipy"):
        expiry_to_indices = {}

        for i, caplet in enumerate(self.caplets):
            if caplet.expiry not in expiry_to_indices:
                expiry_to_indices[caplet.expiry] = [i]
            else:
                expiry_to_indices[caplet.expiry].append(i)

        for expiry, indices in expiry_to_indices.items():
            caplets = [self.caplets[i] for i in indices]
            calibrator = Caplet3MVolCalibrator(caplets, self.ibor_curve)
            self.models[expiry] = calibrator.calibrate(engine=engine)

    def get_vol(self, expiry, strike, forward):
        """Return interpolated vol for a given expiry/strike"""
        if not self.models:
            raise Exception("Model is not yet calibrated, run calibrate() first")

        i, point = 0, 0
        expiries = sorted(list(self.models.keys()))
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

    def plot_calibrated_vol_surface(self, expiry_start, expiry_end, strike_start, strike_end):
        if not self.models:
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
