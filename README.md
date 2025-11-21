# QuantFin

> ⚠️ **Disclaimer:** QuantFin is an educational project. It is **not intended for production use** or for making real financial decisions. Use at your own risk. This library is designed for learning, experimentation, and research purposes only.

QuantFin is a lightweight Python library for interest-rate derivatives and curves.  
It provides tools for building discount and forecasting curves, pricing standard interest-rate instruments, and exploring volatility modeling.  
The library is designed to be **educational, modular, and extensible**, making it easy to experiment with multi-curve frameworks and volatility calibration techniques.

---

## Features

### Curve Construction & Instrument Pricing
- OIS discounting curve construction
- IBOR forecasting curve (currently 3M)
- Sequential curve bootstrapping
- Discount factor interpolation
- Swap pricing: OIS swaps and 3M swaps

### Volatility & Calibration
- Generic volatility surface and calibrator
- SABR-style parameter fitting to market volatilities
- Product-specific calibration (caplets, swaptions) planned for future releases

---

## Quick Start

### Install
```
pip install -r requirements.txt
```

### Example: Bootstrapping Swap Curves
See: `examples/example_bootstrap.py`

```python
from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M

ois_swaps = [...]
swaps3m = [...]

bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
curves = bootstrapper.fit()

ois_curve = curves["ois"]
ibor_curve = curves["3m"]

print(ois_curve.df(1.0))
print(ibor_curve.forward_rate(1.0, 1.25))
```

### Example: Pricing Swaps  
See: `examples/example_bootstrap.py`

```python
ois_swap = OISSwap(3.0, 0.0023, 100)
price = ois_swap.price(ois_curve)

swap3m = Swap3M(3.0, 0.005, 100)
price = swap3m.price(ois_curve, ibor_curve)
```

### Example: Volatility Calibration
See: `examples/example_vol_calibration.py`

```python
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
vol_surface.calibrate()

print("Implied vol for T=1.5, K=102, F=98.5 is " + str(vol_surface.get_vol(1.5, 102, 98.5)))
print("Implied vol for T=1, K=100, F=99 is " + str(vol_surface.get_vol(1, 100, 99)))
print("Implied vol for T=2, K=105, F=98 is " + str(vol_surface.get_vol(2, 105, 98)))
```

---

# Future Work

### 1. Bootstrapping Swap Curves
- Interpolation for missing tenors and broken-tenor instruments
- Support additional IBOR tenors (1m, 6m) via basis swaps
- Implement multiple interpolation techniques (linear, spline, monotone)

### 2. Volatility Calibration
- Pricing and Product-specific SABR calibration for:
  - Caplets
  - Swaptions
- Implement extrapolation logic for strikes/expiries beyond market data

### 3. Risk Greeks
- Develop library for calculating delta, gamma, vega, and other risk measures

### 4. Monte Carlo Pricing
- Generic Monte Carlo engine for pricing more complex instruments

### 5. Performance & Vectorisation
- Profile calibration and bootstrapping routines
- Optimize using vectorised operations or JIT compilation

### 6. Documentation & Readability
- Add detailed docstrings to all core classes/functions
- Enhance README with diagrams illustrating module interactions

### 7. Real Market Data Integration
- Enable calibration and pricing using live market data from APIs

### 8. Risk Scenarios
- Implement scenario analysis: shock interest rates, re-bootstrap, shock volatilities
- Visualize and quantify PnL/risk impact

---

# Referenced Literature

### Bootstrapping
- Interpolation Methods for Curve Construction by Hagan
- Interest Rate Bootstrapping Explained by XAIA Investment
- A Teaching Note on Pricing and Valuing Interest Rate Swaps using LIBOR and OIS Discounting by Donald J. Smith

### Volatility Surface Calibration
- Managing Smile Risk by Hagan
- Equivalent Black Volatilities by Hagan
