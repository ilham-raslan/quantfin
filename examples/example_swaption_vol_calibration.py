from examples.data.markets import OIS_FUTURES, OIS_SWAPS, SWAPS_3M, SWAPTIONS_3M
from quantfin.curves.curve_manager import CurveManager
from quantfin.vol.swaption3m_vol_surface import Swaption3MVolSurface

ois_futures = OIS_FUTURES
ois_swaps = OIS_SWAPS
swaps3m = SWAPS_3M

swaptions = SWAPTIONS_3M

# Build the OIS and 3m Ibor curve needed to price the caplet
curve_manager = CurveManager()
curves = curve_manager.build(ois_swaps, swaps3m, model="log_linear_bootstrapped")

ois_curve = curves["ois"]
ibor3m_curve = curves["3m"]

# Build the vol surface
swaption3m_vol_surface =  Swaption3MVolSurface(swaptions, ibor3m_curve, ois_curve)
# Options:
# scipy: Standard python library
# gauss_newton: Unconstrained optimisation self-implemented
# levenberg_marquardt: Unconstrained optimisation self-implemented
# sqp: Constrained optimisation self-implemented
swaption3m_vol_surface.calibrate(engine="sqp")

vol = swaption3m_vol_surface.get_vol(1,2, 0.02, 0.02)
