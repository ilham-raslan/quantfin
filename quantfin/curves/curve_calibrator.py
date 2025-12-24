import numpy as np
from scipy.optimize import least_squares

from quantfin.optimiser.gauss_newton_optimiser import GaussNewtonOptimiser
from quantfin.optimiser.levenberg_marquardt_optimiser import LevenbergMarquardtOptimiser
from quantfin.optimiser.sqp_optimiser import SQPOptimiser
from quantfin.vol.vol_model import VolModel


class CurveCalibrator:
    """Generic CurveCalibrator class"""

    def __init__(self, instruments):
        self.instruments = instruments

    def residuals(self, params, *args):
        pass

    def calibrate(self, engine="scipy"):
        pass
