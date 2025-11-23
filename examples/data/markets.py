from quantfin.instruments.caplet_3m import Caplet3M
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M

OIS_SWAPS = [
    OISSwap(0.25, 0.010),
    OISSwap(0.50, 0.020),
    OISSwap(0.75, 0.030),
    OISSwap(1.00, 0.050),
    OISSwap(1.25, 0.070),
    OISSwap(1.50, 0.090),
    OISSwap(1.75, 0.0110),
    OISSwap(2.00, 0.0130),
    OISSwap(2.25, 0.0155),
    OISSwap(2.50, 0.0180),
    OISSwap(2.75, 0.0205),
    OISSwap(3.00, 0.0230),
    OISSwap(3.25, 0.0260),
    OISSwap(3.50, 0.0290),
    OISSwap(3.75, 0.0320),
    OISSwap(4.00, 0.0350),
    OISSwap(4.25, 0.0385),
    OISSwap(4.50, 0.0420),
    OISSwap(4.75, 0.0455),
    OISSwap(5.00, 0.0490)
]

SWAPS_3M = [
    Swap3M(0.25, 0.010),
    Swap3M(0.50, 0.012),
    Swap3M(0.75, 0.015),
    Swap3M(1.00, 0.030),
    Swap3M(1.25, 0.035),
    Swap3M(1.50, 0.038),
    Swap3M(1.75, 0.039),
    Swap3M(2.00, 0.040),
    Swap3M(2.25, 0.042),
    Swap3M(2.50, 0.045),
    Swap3M(2.75, 0.048),
    Swap3M(3.00, 0.050),
    Swap3M(3.25, 0.053),
    Swap3M(3.50, 0.056),
    Swap3M(3.75, 0.060),
    Swap3M(4.00, 0.063),
    Swap3M(4.25, 0.067),
    Swap3M(4.50, 0.070),
    Swap3M(4.75, 0.073),
    Swap3M(5.00, 0.075)
]

CAPLETS_3M = [
    Caplet3M(0.25, 0.008, 1, 0.145),
    Caplet3M(0.25, 0.010, 1, 0.135),
    Caplet3M(0.25, 0.012, 1, 0.148),

    Caplet3M(0.50, 0.007, 1, 0.150),
    Caplet3M(0.50, 0.011, 1, 0.140),
    Caplet3M(0.50, 0.015, 1, 0.152),

    Caplet3M(1.0, 0.009, 1, 0.165),
    Caplet3M(1.0, 0.013, 1, 0.150),
    Caplet3M(1.0, 0.017, 1, 0.162),

    Caplet3M(2.0, 0.012, 1, 0.185),
    Caplet3M(2.0, 0.017, 1, 0.170),
    Caplet3M(2.0, 0.022, 1, 0.178),

    Caplet3M(3.0, 0.014, 1, 0.205),
    Caplet3M(3.0, 0.020, 1, 0.190),
    Caplet3M(3.0, 0.026, 1, 0.198),

    Caplet3M(4.75, 0.015, 1, 0.230),
    Caplet3M(4.75, 0.023, 1, 0.210),
    Caplet3M(4.75, 0.031, 1, 0.220),
]
