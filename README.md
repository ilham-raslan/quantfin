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

# QuantFin Examples

---

## Example 1: Bootstrapping Swap Curves

See: `examples/example_bootstrap.py`

```python
from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M

# Explicit market data
ois_swaps = [
    OISSwap(0.25, 0.010),
    OISSwap(0.50, 0.020),
    OISSwap(0.75, 0.030),
    OISSwap(1.00, 0.050),
    OISSwap(1.25, 0.070),
    OISSwap(1.50, 0.090)
]

swaps3m = [
    Swap3M(0.25, 0.010),
    Swap3M(0.50, 0.012),
    Swap3M(0.75, 0.015),
    Swap3M(1.00, 0.030),
    Swap3M(1.25, 0.035),
    Swap3M(1.50, 0.038)
]

bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
curves = bootstrapper.fit()

ois_curve = curves["ois"]
ibor_curve = curves["3m"]

print("Discount factor for T=1.0:", ois_curve.df(1.0))
print("Forward rate from 1.0 to 1.25:", ibor_curve.forward_rate(1.0, 1.25))
```

---

## Example 2: Pricing Swaps

See: `examples/example_bootstrap.py`

```python
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M

# Assume curves are already bootstrapped
ois_curve = ...
ibor_curve = ...

# Price an OIS swap
ois_swap = OISSwap(3.0, 0.023, 100)
price = ois_swap.price(ois_curve)
print("OIS Swap price:", price)

# Price a 3M swap
swap3m = Swap3M(3.0, 0.050, 100)
price = swap3m.price(ois_curve, ibor_curve)
print("3M Swap price:", price)
```

---

## Example 3: Volatility Calibration

See: `examples/example_vol_calibration.py`

```python
from quantfin.vol.vol_surface import VolSurface

market_options = [
    { "expiry": 1.0, "strike": 100, "market_vol": 0.2, "forward": 99 },
    { "expiry": 1.0, "strike": 105, "market_vol": 0.22, "forward": 99 },
    { "expiry": 2.0, "strike": 100, "market_vol": 0.21, "forward": 98 },
    { "expiry": 2.0, "strike": 105, "market_vol": 0.23, "forward": 98 }
]

expiry_list = [opt["expiry"] for opt in market_options]
strike_list = [opt["strike"] for opt in market_options]
market_vol_list = [opt["market_vol"] for opt in market_options]
forward_list = [opt["forward"] for opt in market_options]

vol_surface = VolSurface(expiry_list, strike_list, market_vol_list, forward_list)
vol_surface.calibrate()

print("Implied vol for T=1.5, K=102, F=98.5:", vol_surface.get_vol(1.5, 102, 98.5))
print("Implied vol for T=1, K=100, F=99:", vol_surface.get_vol(1, 100, 99))
print("Implied vol for T=2, K=105, F=98:", vol_surface.get_vol(2, 105, 98))
```

---

## Example 4: Pricing a Caplet

See: `examples/example_caplet_pricing.py`

```python
from quantfin.vol.caplet3m_vol_surface import Caplet3MVolSurface
from quantfin.instruments.caplet_3m import Caplet3M
from quantfin.instruments.ois_swap import OISSwap
from quantfin.instruments.swap_3m import Swap3M
from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper

ois_swaps = [...]     # List of OISSwap instruments
swaps3m = [...]       # List of 3M Swap instruments
caplets_3m = [...]    # List of Caplet3M instruments

bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
curves = bootstrapper.fit()
ois_curve = curves["ois"]
ibor_curve = curves["3m"]

vol_surface = Caplet3MVolSurface(caplets=caplets_3m, ibor_curve=ibor_curve)
vol_surface.calibrate()

# Price a single caplet
caplet = Caplet3M(1.5, 0.042, 1, None)  # expiry, strike, notional, market_vol placeholder
price = caplet.price(ois_curve, ibor_curve, vol_surface)
print("Caplet price:", price)
```

---

### Notes

* Explicit market data is included for Example 1 to show how bootstrapping works. Other examples use placeholders (`[...]`) to focus on **API usage** rather than data preparation.

# Future Work

### 1. Bootstrapping Swap Curves
- Currently bootstraps OIS from quarterly paying OIS swaps at all tenors which is unrealistic, this should use more realistic OIS instruments
- Support additional IBOR tenors (1m, 6m) via basis swaps
- Implement multiple interpolation techniques (linear, spline, monotone)

### 2. Volatility Calibration
- Pricing and Product-specific SABR calibration for:
  - Swaptions

### 3. Accuracy Metrics
- Tests for interpolated values, not just at knots
- Regression tests

### 4. Risk Greeks
- Develop library for calculating delta, gamma, vega, and other risk measures

### 5. Monte Carlo Pricing
- Generic Monte Carlo engine for pricing more complex instruments

### 6. Performance & Vectorisation
- Profile calibration and bootstrapping routines
- Optimise using vectorised operations or

### 7. Documentation & Readability
- Add detailed docstrings to all core classes/functions
- Enhance README with diagrams illustrating module interactions

### 8. Real Market Data Integration
- Enable calibration and pricing using live market data from APIs

### 9. Risk Scenarios
- Implement scenario analysis: shock interest rates, re-bootstrap, shock volatilities
- Visualise and quantify PnL/risk impact

---

# Referenced Literature

### Bootstrapping
- Interest Rate Bootstrapping Explained by XAIA Investment
- A Teaching Note on Pricing and Valuing Interest Rate Swaps using LIBOR and OIS Discounting by Donald J. Smith
- Interpolation Methods for Curve Construction by Hagan
- Interest Rate Models - Theory and Practice by Brigo and Mercurio
- Options, Futures and Other Derivatives by Hull

### Volatility Surface Calibration
- Managing Smile Risk by Hagan
- Equivalent Black Volatilities by Hagan
- Options, Futures and Other Derivatives by Hull
