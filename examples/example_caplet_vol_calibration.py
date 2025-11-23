from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.instruments.caplet_3m import Caplet3M
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M
from quantfin.vol.caplet3m_vol_surface import Caplet3MVolSurface


ois_swaps = [OISSwap(tenor, rate) for tenor, rate in [
    (0.25, 0.0050), (0.50, 0.0060), (0.75, 0.0070), (1.00, 0.0080),
    (1.25, 0.0090), (1.50, 0.0100), (1.75, 0.0110), (2.00, 0.0120),
    (2.25, 0.0130), (2.50, 0.0140), (2.75, 0.0150), (3.00, 0.0160),
    (3.25, 0.0170), (3.50, 0.0180), (3.75, 0.0190), (4.00, 0.0200),
    (4.25, 0.0210), (4.50, 0.0220), (4.75, 0.0230), (5.00, 0.0240),
    (5.25, 0.0250)
]]

swaps3m = [Swap3M(tenor, rate) for tenor, rate in [
    (0.25, 0.0060), (0.50, 0.0070), (0.75, 0.0080), (1.00, 0.0090),
    (1.25, 0.0100), (1.50, 0.0110), (1.75, 0.0120), (2.00, 0.0130),
    (2.25, 0.0140), (2.50, 0.0150), (2.75, 0.0160), (3.00, 0.0170),
    (3.25, 0.0180), (3.50, 0.0190), (3.75, 0.0200), (4.00, 0.0210),
    (4.25, 0.0220), (4.50, 0.0230), (4.75, 0.0240), (5.00, 0.0250),
    (5.25, 0.0260)
]]

caplets = [Caplet3M(expiry, strike, notional, market_vol) for expiry, strike, notional, market_vol in [
    (0.25, 0.0033, 0.25, 0.14),
    (0.25, 0.0044, 0.25, 0.12),
    (0.25, 0.0055, 0.25, 0.11),
    (0.25, 0.0066, 0.25, 0.115),
    (0.25, 0.00825, 0.25, 0.13),

    (1.0, 0.0054, 0.25, 0.20),
    (1.0, 0.0072, 0.25, 0.17),
    (1.0, 0.0090, 0.25, 0.15),
    (1.0, 0.0108, 0.25, 0.155),
    (1.0, 0.0135, 0.25, 0.18),

    (2.0, 0.0072, 0.25, 0.23),
    (2.0, 0.0108, 0.25, 0.19),
    (2.0, 0.0120, 0.25, 0.175),
    (2.0, 0.0150, 0.25, 0.185),
    (2.0, 0.0180, 0.25, 0.21),

    (5.0, 0.0108, 0.25, 0.30),
    (5.0, 0.0162, 0.25, 0.245),
    (5.0, 0.0180, 0.25, 0.22),
    (5.0, 0.0216, 0.25, 0.235),
    (5.0, 0.0270, 0.25, 0.265)
]]

# Build the OIS and 3m Ibor curve needed to price the caplet
bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
curves = bootstrapper.fit()

ois_curve = curves["ois"]
ibor3m_curve = curves["3m"]

# Build the vol surface
caplet3m_vol_surface =  Caplet3MVolSurface(caplets, ibor3m_curve)
caplet3m_vol_surface.calibrate()

caplet3m_vol_surface.plot_calibrated_vol_surface(0, 5, 0.001, 0.05)
