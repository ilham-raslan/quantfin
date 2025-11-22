from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M

OIS_SWAPS = [
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

SWAPS_3M = [
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

SABR_DATA = [
    { "expiry": 1.0, "strike": 100, "market_vol": 0.2, "forward": 99 },
    { "expiry": 1.0, "strike": 105, "market_vol": 0.22, "forward": 99  },
    { "expiry": 2.0, "strike": 100, "market_vol": 0.21, "forward": 98  },
    { "expiry": 2.0, "strike": 105, "market_vol": 0.23, "forward": 98  }
]
