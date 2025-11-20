from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M
import pytest

def test_bootstrapper():
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