from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.curves.ibor_curve_calibrator import IBORCurveCalibrator
from quantfin.curves.ois_curve_calibrator import OISCurveCalibrator


class CurveManager:
    def build(self, ois_swaps, swaps3m, model="log_linear_bootstrapped", calibration_engine="scipy"):
        if model == "log_linear_bootstrapped":
            bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
            curves = bootstrapper.fit()

            return {
                "ois": curves["ois"],
                "3m": curves["3m"]
            }
        elif model == "nelson_siegel":
            ois_curve_calibrator = OISCurveCalibrator(ois_swaps)
            ois_curve = ois_curve_calibrator.calibrate(calibration_engine)

            ibor_curve_calibrator = IBORCurveCalibrator(swaps3m, ois_curve)
            ibor_curve = ibor_curve_calibrator.calibrate(calibration_engine)

            return {
                "ois": ois_curve,
                "3m": ibor_curve
            }
        else:
            raise ValueError(f"Curve build mode {model} is not supported")