import numpy as np
from scipy.optimize import least_squares

from quantfin.curves.curve import Curve
from quantfin.curves.nelson_siegel_df_provider import NelsonSiegelDFProvider
from quantfin.optimiser.gauss_newton_optimiser import GaussNewtonOptimiser
from quantfin.optimiser.levenberg_marquardt_optimiser import LevenbergMarquardtOptimiser
from quantfin.optimiser.sqp_optimiser import SQPOptimiser
from quantfin.vol.vol_model import VolModel


class OISCurveCalibrator:
    """OISCurveCalibrator class"""

    def __init__(self, instruments):
        self.instruments = instruments

    def residuals(self, params, *args):
        beta0, beta1, beta2, tau = params
        ois_curve = Curve(NelsonSiegelDFProvider(beta0, beta1, beta2, tau))
        instruments = args

        return np.array([
            instrument.price(ois_curve)
            for instrument in instruments
        ])

    def calibrate(self, engine="scipy"):
        if engine == "scipy":
            instruments = np.array(self.instruments)

            # initial guesses
            x0 = np.array([0.025, 0, 0, 2])

            result = least_squares(
                fun=self.residuals,
                x0=x0,
                args=instruments,
                method='trf',
                verbose=1
            )

            residuals = result.fun

            # RMS error
            rms_error = np.sqrt(np.mean(residuals ** 2))
            print("RMS error:", rms_error)

            # Maximum absolute residual
            max_error = np.max(np.abs(residuals))
            print("Max absolute residual:", max_error)

            # Fitted parameters
            beta0_fit, beta1_fit, beta2_fit, tau_fit = result.x
            print("Fitted params:", beta0_fit, beta1_fit, beta2_fit, tau_fit)
        elif engine == "gauss_newton":
            optimiser = GaussNewtonOptimiser()
            x0 = np.array([0.025, 0, 0, 2])
            params = optimiser.optimise(
                x0,
                self.residuals,
                self.instruments
            )
            beta0_fit, beta1_fit, beta2_fit, tau_fit = params
            print("Fitted params:", beta0_fit, beta1_fit, beta2_fit, tau_fit)
        elif engine == "levenberg_marquardt":
            optimiser = LevenbergMarquardtOptimiser()
            x0 = np.array([0.025, 0, 0, 2])
            params = optimiser.optimise(
                x0,
                self.residuals,
                self.instruments
            )
            beta0_fit, beta1_fit, beta2_fit, tau_fit = params
            print("Fitted params:", beta0_fit, beta1_fit, beta2_fit, tau_fit)
        else:
            raise Exception("Calibration engine " + engine + " unsupported")

        return Curve(NelsonSiegelDFProvider(beta0_fit, beta1_fit, beta2_fit, tau_fit))
