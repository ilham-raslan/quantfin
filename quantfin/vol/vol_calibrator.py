import numpy as np
from scipy.optimize import least_squares

from quantfin.optimiser.gauss_newton_optimiser import GaussNewtonOptimiser
from quantfin.optimiser.levenberg_marquardt_optimiser import LevenbergMarquardtOptimiser
from quantfin.optimiser.sqp_optimiser import SQPOptimiser
from quantfin.vol.vol_model import VolModel


class VolCalibrator:
    """Generic VolCalibrator class"""

    def __init__(self, expiries, strikes, market_vols, forwards):
        self.expiries = expiries
        self.strikes = strikes
        self.market_vols = market_vols
        self.forwards = forwards

    def residuals(self, params, expiries, strikes, forwards, market_vols):
        alpha, rho, nu = params
        model = VolModel(alpha, rho, nu)

        return np.array([
            model.get_vol(T, K, F) - market_vol
            for T, K, F, market_vol in zip(expiries, strikes, forwards, market_vols)
        ])

    def calibrate(self, engine="scipy"):
        if engine == "scipy":
            expiries = np.array(self.expiries)
            strikes = np.array(self.strikes)
            forwards = np.array(self.forwards)
            market_vols = np.array(self.market_vols)

            # initial guesses
            x0 = np.array([0.2, 0.2, 0.5])

            lower = [1e-8, -0.999, 1e-8]
            upper = [10.0, 0.999, 5.0]

            result = least_squares(
                fun=self.residuals,
                x0=x0,
                bounds=(lower, upper),
                args=(expiries, strikes, forwards, market_vols),
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
            alpha_fit, rho_fit, nu_fit = result.x
            print("Fitted params:", alpha_fit, rho_fit, nu_fit)
        elif engine == "gauss_newton":
            optimiser = GaussNewtonOptimiser(self.residuals, self.expiries, self.strikes, self.market_vols, self.forwards)
            x0 = np.array([0.2, 0.2, 0.5])
            params = optimiser.optimise(x0)
            alpha_fit, rho_fit, nu_fit = params
            print("Fitted params:", alpha_fit, rho_fit, nu_fit)
        elif engine == "levenberg_marquardt":
            optimiser = LevenbergMarquardtOptimiser(self.residuals, self.expiries, self.strikes, self.market_vols, self.forwards)
            x0 = np.array([0.2, 0.2, 0.5])
            params = optimiser.optimise(x0)
            alpha_fit, rho_fit, nu_fit = params
        elif engine == "gauss_newton":
            optimiser = GaussNewtonOptimiser(self.residuals, self.expiries, self.strikes, self.market_vols, self.forwards)
            x0 = np.array([0.2, 0.2, 0.5])
            params = optimiser.optimise(x0)
            alpha_fit, rho_fit, nu_fit = params
            print("Fitted params:", alpha_fit, rho_fit, nu_fit)
        elif engine == "sqp":
            optimiser = SQPOptimiser(self.residuals, self.expiries, self.strikes, self.market_vols, self.forwards)
            # x0 = np.array([0.00000001, 0.8, 0.0000001]) # Below is actual decent guess but this one is for testing constrained optimisation
            x0 = np.array([0.2, 0.2, 0.5])
            params = optimiser.optimise(x0)
            alpha_fit, rho_fit, nu_fit = params
            print("Fitted params:", alpha_fit, rho_fit, nu_fit)
        else:
            raise Exception("Calibration engine " + engine + " unsupported")

        return VolModel(alpha_fit, rho_fit, nu_fit)
