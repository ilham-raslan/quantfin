import pytest
from quantfin.vol.vol_surface import VolSurface
from quantfin.vol.vol_calibrator import VolCalibrator

def test_vol_surface_add_get():
    surface = VolSurface()
    surface.add_market_vol(expiry=1.0, strike=100, vol=0.2, forward=99)
    surface.calibrate()
    vol = surface.get_vol(expiry=1.0, strike=100, forward=99)
    assert vol == pytest.approx(0.2)
