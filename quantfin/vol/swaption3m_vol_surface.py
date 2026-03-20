import matplotlib.pyplot as plt
import numpy as np

from quantfin.vol.caplet3m_vol_calibrator import Caplet3MVolCalibrator
from quantfin.vol.swaption3m_vol_calibrator import Swaption3MVolCalibrator


class Swaption3MVolSurface:
    """Represents a volatility surface for 3m swaptions: vol = f(strike, expiry)"""

    def __init__(self, swaptions=None, ibor_curve=None, ois_curve=None):
        self.swaptions = swaptions if swaptions is not None else []
        self.ibor_curve = ibor_curve
        self.ois_curve = ois_curve
        self.models = {}

    def add_swaption(self, swaption):
        self.swaptions.append(swaption)

    def calibrate(self, engine="scipy"):
        expiry_tenor_to_indices = {}

        for i, swaption in enumerate(self.swaptions):
            if (swaption.expiry, swaption.tenor) not in expiry_tenor_to_indices:
                expiry_tenor_to_indices[(swaption.expiry, swaption.tenor)] = [i]
            else:
                expiry_tenor_to_indices[(swaption.expiry, swaption.tenor)].append(i)

        for expiry_tenor, indices in expiry_tenor_to_indices.items():
            expiry, tenor = expiry_tenor
            swaptions = [self.swaptions[i] for i in indices]
            calibrator = Swaption3MVolCalibrator(swaptions, self.ibor_curve, self.ois_curve)
            self.models[(expiry, tenor)] = calibrator.calibrate(engine=engine)

    def get_vol(self, expiry, tenor, strike, forward):
        """Return interpolated vol for a given expiry/strike/tenor"""
        if not self.models:
            raise Exception("Model is not yet calibrated, run calibrate() first")

        def find_bracket(x, grid):
            for i, point in enumerate(grid):
                if x == point:
                    return point, point
                elif x < point:
                    return grid[i - 1], point

            return grid[-1], grid[-1]

        def weight(x, x1, x2):
            if x1 == x2:
                return 1.0
            return (x - x1) / (x2 - x1)

        expiries = sorted(set(e for e, _ in self.models.keys()))
        tenors = sorted(set(t for _, t in self.models.keys()))
        T1, T2 = find_bracket(expiry, expiries)
        tau1, tau2 = find_bracket(tenor, tenors)

        w_T = weight(expiry, T1, T2)
        w_tau = weight(tenor, tau1, tau2)

        v11 = self.models[(T1, tau1)].get_vol(T1, strike, forward)
        v12 = self.models[(T1, tau2)].get_vol(T1, strike, forward)
        v21 = self.models[(T2, tau1)].get_vol(T2, strike, forward)
        v22 = self.models[(T2, tau2)].get_vol(T2, strike, forward)

        return (
            (1 - w_T) * (1 - w_tau) * v11 +
            (1 - w_T) * (w_tau) * v12 +
            (w_T) * (1 - w_tau) * v21 +
            (w_T) * (w_tau) * v22
        )

    def plot_calibrated_vol_surface(self, expiry_start, expiry_end, strike_start, strike_end):
        raise NotImplementedError("Not implemented")
        # if not self.models:
        #     raise Exception("Model is not yet calibrated, run calibrate() first")
        #
        # expiry_intervals = 100
        # expiries = np.linspace(expiry_start, expiry_end, expiry_intervals)
        #
        # strike_intervals = 100
        # strikes = np.linspace(strike_start, strike_end, strike_intervals)
        #
        # x, y = np.meshgrid(expiries, strikes, indexing="ij")
        # z = np.zeros((len(expiries), len(strikes)))
        #
        # for i, t in enumerate(expiries):
        #     for j, k in enumerate(strikes):
        #         f = self.ibor_curve.forward_rate(t, t + 0.25)
        #         z[i, j] = self.get_vol(t, k, f)
        #
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # ax.plot_surface(x, y, z, cmap="viridis")
        # ax.set_xlabel("Expiry (years)")
        # ax.set_ylabel("Strike")
        # ax.set_zlabel("Volatility")
        # ax.set_title("Volatility Surface")
        #
        # plt.show()
