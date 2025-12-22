from examples.data.markets import OIS_FUTURES, OIS_SWAPS, SWAPS_3M, CAPLETS_3M
from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.vol.caplet3m_vol_surface import Caplet3MVolSurface

ois_futures = OIS_FUTURES
ois_swaps = OIS_SWAPS
swaps3m = SWAPS_3M

caplets = CAPLETS_3M

# Build the OIS and 3m Ibor curve needed to price the caplet
bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
curves = bootstrapper.fit()

ois_curve = curves["ois"]
ibor3m_curve = curves["3m"]

# Build the vol surface
caplet3m_vol_surface =  Caplet3MVolSurface(caplets, ibor3m_curve)
# Options:
# scipy: Standard python library
# gauss_newton: Unconstrained optimisation self-implemented
# levenberg_marquardt: Unconstrained optimisation self-implemented
# sqp: Constrained optimisation self-implemented
caplet3m_vol_surface.calibrate(engine="sqp")

caplet3m_vol_surface.plot_calibrated_vol_surface(0, 5, 0.001, 0.05)
