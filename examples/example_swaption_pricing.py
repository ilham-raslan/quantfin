from examples.data.markets import OIS_SWAPS, SWAPS_3M, SWAPTIONS_3M
from quantfin.curves.curve_manager import CurveManager
from quantfin.instruments.swaption_3m import Swaption3M
from quantfin.vol.swaption3m_vol_surface import Swaption3MVolSurface

# Generate caplet market data
ois_swaps = OIS_SWAPS
swaps3m = SWAPS_3M
swaptions3m = SWAPTIONS_3M

# Build the OIS and 3m Ibor curve needed to price the caplet
curve_manager = CurveManager()
curves = curve_manager.build(ois_swaps, swaps3m, model="log_linear_bootstrapped")

ois_curve = curves["ois"]
ibor3m_curve = curves["3m"]

# Fake vol surface for now
# Build the vol surface
swaption3m_vol_surface = Swaption3MVolSurface(swaptions3m, ibor3m_curve, ois_curve)
swaption3m_vol_surface.calibrate()

# price an example swaption
swaption3m = Swaption3M(1, 2, 0.042, 100)
swaption3m_price = swaption3m.price(ois_curve, ibor3m_curve, swaption3m_vol_surface)
print("2y into 2y swaption with strike 0.042 and notional 100 cost " + str(swaption3m_price))
