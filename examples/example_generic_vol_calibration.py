from quantfin.vol.vol_surface import VolSurface

market_options = [
    { "expiry": 1.0, "strike": 100, "market_vol": 0.2, "forward": 99 },
    { "expiry": 1.0, "strike": 105, "market_vol": 0.22, "forward": 99  },
    { "expiry": 2.0, "strike": 100, "market_vol": 0.21, "forward": 98  },
    { "expiry": 2.0, "strike": 105, "market_vol": 0.23, "forward": 98  },
]

expiry_list = [opt["expiry"] for opt in market_options]
strike_list = [opt["strike"] for opt in market_options]
market_vol_list = [opt["market_vol"] for opt in market_options]
forward_list = [opt["forward"] for opt in market_options]

vol_surface = VolSurface(expiry_list, strike_list, market_vol_list, forward_list)

vol_surface.calibrate(engine="scipy")

print("Implied vol for T=1.5, K=102, F=98.5 is " + str(vol_surface.get_vol(1.5, 102, 98.5)))
print("Implied vol for T=1, K=100, F=99 is " + str(vol_surface.get_vol(1, 100, 99)))
print("Implied vol for T=2, K=105, F=98 is " + str(vol_surface.get_vol(2, 105, 98)))
