from examples.data.markets import OIS_SWAPS, SWAPS_3M
from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.curves.curve_manager import CurveManager
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M

# Generate curves from stored test data
ois_swaps = OIS_SWAPS
swaps3m = SWAPS_3M

curve_manager = CurveManager()
curves = curve_manager.build(ois_swaps, swaps3m)

ois_curve = curves["ois"]
ibor3m_curve = curves["3m"]

# price an example OIS Swap
ois_swap = OISSwap(3, 0.021, 100)
ois_swap_price = ois_swap.price(ois_curve)
print("3y ois swap with notional 100 and fixed rate 0.021 is priced at " + str(ois_swap_price))

# price an example 3m Ibor Swap
ibor3m_swap = Swap3M(3, 0.03, 100)
ibor3m_swap_price = ibor3m_swap.price(ois_curve, ibor3m_curve)
print("3y ibor 3m swap with notional 100 and fixed rate 0.03 is priced at " + str(ibor3m_swap_price))
