from quantfin.curves.bootstrapper import MultiCurveBootstrapper
from quantfin.curves.instruments import OISSwap, Swap3M

ois_swaps = [
    OISSwap(0.5, 0.0010),   # 6M OIS at 0.10%
    OISSwap(1.0, 0.0015),   # 1Y  OIS at 0.15%
    OISSwap(2.0, 0.0020),   # 2Y  OIS at 0.20%
    OISSwap(3.0, 0.0027),   # 3Y  OIS at 0.27%
    OISSwap(4.0, 0.0033),   # 4Y  OIS at 0.33%
    OISSwap(5.0, 0.0040)    # 5Y  OIS at 0.40%
]

swaps3m = [
    Swap3M(1.0, 0.0030),    # 1Y  3M swap at 0.30%
    Swap3M(2.0, 0.0040),    # 2Y  3M swap at 0.40%
    Swap3M(5.0, 0.0075)     # 5Y  3M swap at 0.75%
]

bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)

ois_curve = bootstrapper.bootstrap_ois()
print(ois_curve.df)

# curves = bootstrapper.fit()
#
# ois_curve = curves["ois"]
# ibor3m_curve = curves["3m"]
#
# df_1y = ois_curve.df(1.0)
# fwd = ibor3m_curve.forward_rate(1.0, 1.25)
