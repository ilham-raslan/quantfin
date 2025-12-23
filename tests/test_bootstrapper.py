import pytest

from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.curves.curve_manager import CurveManager
from quantfin.instruments.ois_future import OISFuture
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M


def test_bootstrapper_rates():
    ois_swaps = [
        OISSwap(2.00, 0.0220),
        OISSwap(3.00, 0.0240)
    ]

    swaps3m = [
        Swap3M(0.25, 0.0230)
    ]

    curve_manager = CurveManager()
    curves = curve_manager.build(ois_swaps, swaps3m, mode="bootstrap")

    ois_curve = curves["ois"]
    ibor3m_curve = curves["3m"]

    assert ois_curve.df(2) == pytest.approx(0.9564787)
    assert ibor3m_curve.forward_rate(0, 0.25) == pytest.approx(0.023)

def test_bootstrapper_swap_prices():
    ois_futures = [
        OISFuture(0.25, 0.9810),  # implies 1.90%
        OISFuture(0.50, 0.9805),  # implies 1.95%
        OISFuture(0.75, 0.9800),  # implies 2.00%
        OISFuture(1.00, 0.9795),  # implies 2.05%
        OISFuture(1.25, 0.9790),  # implies 2.10%
        OISFuture(1.50, 0.9785),  # implies 2.15%
        OISFuture(1.75, 0.9780)  # implies 2.20%
    ]

    ois_swaps = [
        OISSwap(2.00, 0.0220),
        OISSwap(3.00, 0.0240),
    ]

    swaps3m = [
        Swap3M(0.25, 0.023),
        Swap3M(0.50, 0.024)
    ]

    ois_instruments = ois_futures + ois_swaps

    curve_manager = CurveManager()
    curves = curve_manager.build(ois_instruments, swaps3m, mode="bootstrap")

    ois_curve = curves["ois"]
    ibor3m_curve = curves["3m"]

    # swaps used in bootstrapping should have pv's close to 0
    for swap in ois_swaps:
        pv_model = swap.price(ois_curve)
        assert abs(pv_model) < 1e-3

    for swap in swaps3m:
        pv_model = swap.price(ois_curve, ibor3m_curve)
        assert abs(pv_model) < 1e-3
