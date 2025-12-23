from examples.data.markets import CAPLETS_3M, OIS_SWAPS, SWAPS_3M
from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.curves.curve_manager import CurveManager
from quantfin.instruments.caplet_3m import Caplet3M
from quantfin.vol.caplet3m_vol_surface import Caplet3MVolSurface

# Generate caplet market data
caplets_3m = CAPLETS_3M
ois_swaps = OIS_SWAPS
swaps3m = SWAPS_3M

# Build the OIS and 3m Ibor curve needed to price the caplet
curve_manager = CurveManager()
curves = curve_manager.build(ois_swaps, swaps3m, mode="bootstrap")

ois_curve = curves["ois"]
ibor3m_curve = curves["3m"]

# Build the vol surface
caplet3m_vol_surface =  Caplet3MVolSurface(caplets_3m, ibor3m_curve)
caplet3m_vol_surface.calibrate()

# price an example caplet
caplet3m = Caplet3M(1, 0.008, 100)
caplet3m_price = caplet3m.price(ois_curve, ibor3m_curve, caplet3m_vol_surface)
print("1y caplet with strike 0.008 and notional 100 cost " + str(caplet3m_price))
