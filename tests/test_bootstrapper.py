import pytest

from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M


def test_bootstraper_rates():
    ois_swaps = [
        OISSwap(0.25, 0.00010)
    ]

    swaps3m = [
        Swap3M(0.25, 0.0010)
    ]

    bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
    curves = bootstrapper.fit()

    ois_curve = curves["ois"]
    ibor3m_curve = curves["3m"]

    assert ois_curve.df(0.25) == pytest.approx(0.99997500062)
    assert ibor3m_curve.forward_rate(0, 0.25) == pytest.approx(0.001)

def test_bootstrapper_swap_prices():
    ois_swaps = [
        OISSwap(0.25, 0.0050),
        OISSwap(0.50, 0.0060)
    ]

    swaps3m = [
        Swap3M(0.25, 0.0060),
        Swap3M(0.50, 0.0070)
    ]

    bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
    curves = bootstrapper.fit()

    ois_curve = curves["ois"]
    ibor3m_curve = curves["3m"]

    # swaps used in bootstrapping should have pv's close to 0
    for swap in ois_swaps:
        pv_model = swap.price(ois_curve)
        assert abs(pv_model) < 1e-12

    for swap in swaps3m:
        pv_model = swap.price(ois_curve, ibor3m_curve)
        assert abs(pv_model) < 1e-12
