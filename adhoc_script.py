from quantfin.curves.bootstrapper import MultiCurveBootstrapper
from quantfin.curves.instruments import OISSwap, Swap3M

ois_swaps = [
    OISSwap(0.25, 0.00010),
    OISSwap(0.50, 0.00020),
    OISSwap(0.75, 0.00030),
    OISSwap(1.00, 0.00050),
    OISSwap(1.25, 0.00070),
    OISSwap(1.50, 0.00090),
    OISSwap(1.75, 0.00110),
    OISSwap(2.00, 0.00130),
    OISSwap(2.25, 0.00155),
    OISSwap(2.50, 0.00180),
    OISSwap(2.75, 0.00205),
    OISSwap(3.00, 0.00230),
    OISSwap(3.25, 0.00260),
    OISSwap(3.50, 0.00290),
    OISSwap(3.75, 0.00320),
    OISSwap(4.00, 0.00350),
    OISSwap(4.25, 0.00385),
    OISSwap(4.50, 0.00420),
    OISSwap(4.75, 0.00455),
    OISSwap(5.00, 0.00490)
]

swaps3m = [
    Swap3M(0.25, 0.0010),
    Swap3M(0.50, 0.0012),
    Swap3M(0.75, 0.0015),
    Swap3M(1.00, 0.0030),
    Swap3M(1.25, 0.0035),
    Swap3M(1.50, 0.0038),
    Swap3M(1.75, 0.0039),
    Swap3M(2.00, 0.0040),
    Swap3M(2.25, 0.0042),
    Swap3M(2.50, 0.0045),
    Swap3M(2.75, 0.0048),
    Swap3M(3.00, 0.0050),
    Swap3M(3.25, 0.0053),
    Swap3M(3.50, 0.0056),
    Swap3M(3.75, 0.0060),
    Swap3M(4.00, 0.0063),
    Swap3M(4.25, 0.0067),
    Swap3M(4.50, 0.0070),
    Swap3M(4.75, 0.0073),
    Swap3M(5.00, 0.0075)
]

bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
curves = bootstrapper.fit()

ois_curve = curves["ois"]
ibor3m_curve = curves["3m"]

df_1y = ois_curve.df(1.0)
print("1y ois discounting: " + str(df_1y))

zero = ois_curve.zero_rate(1.5)
print("1.5y ois zero rate: " + str(zero))

fwd = ibor3m_curve.forward_rate(1.0, 1.25)
print("1.0 to 1.25 forward rate: " + str(fwd))
