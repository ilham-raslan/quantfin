import numpy as np
from scipy.optimize import least_squares

from quantfin.curves.curve import Curve
from quantfin.curves.nelson_siegel_curve_model import NelsonSiegelCurveModel
from quantfin.instruments.swap_3m import Swap3M
from quantfin.optimiser.gauss_newton_optimiser import GaussNewtonOptimiser
from quantfin.optimiser.levenberg_marquardt_optimiser import LevenbergMarquardtOptimiser
from quantfin.optimiser.sqp_optimiser import SQPOptimiser
from quantfin.vol.vol_model import VolModel


class IBORCurveCalibrator:
    """IBORCurveCalibrator class"""

    def __init__(self, instruments, ois_curve):
        self.instruments = instruments
        self.ois_curve = ois_curve

    def residuals(self, params, *args):
        beta0, beta1, beta2, tau = params
        ibor_curve = Curve(NelsonSiegelCurveModel(beta0, beta1, beta2, tau))
        instruments, ois_curve = args

        def residual(instrument, ois_curve_inner, ibor_curve_inner):
            if isinstance(instrument, Swap3M):
                return instrument.price(ois_curve_inner, ibor_curve_inner)
            else:
                raise Exception("Instrument " + instrument.__class__.__name__ + " is not supported for OIS curve calibration")

        return np.array([
            residual(instrument, ois_curve, ibor_curve)
            for instrument in instruments
        ])

    def calibrate(self, engine="scipy"):
        if engine == "scipy":
            instruments, ois_curve = np.array(self.instruments), self.ois_curve

            # initial guesses
            x0 = np.array([0.025, 0, 0, 2])

            result = least_squares(
                fun=self.residuals,
                x0=x0,
                args=(instruments, ois_curve),
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
                (self.instruments, self.ois_curve)
            )
            beta0_fit, beta1_fit, beta2_fit, tau_fit = params
            print("Fitted params:", beta0_fit, beta1_fit, beta2_fit, tau_fit)
        elif engine == "levenberg_marquardt":
            optimiser = LevenbergMarquardtOptimiser()
            x0 = np.array([0.025, 0, 0, 2])
            params = optimiser.optimise(
                x0,
                self.residuals,
                (self.instruments, self.ois_curve)
            )
            beta0_fit, beta1_fit, beta2_fit, tau_fit = params
            print("Fitted params:", beta0_fit, beta1_fit, beta2_fit, tau_fit)
        else:
            raise Exception("Calibration engine " + engine + " unsupported")

        return Curve(NelsonSiegelCurveModel(beta0_fit, beta1_fit, beta2_fit, tau_fit))
