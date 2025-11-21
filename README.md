# QuantFin

> ⚠️ **Disclaimer:** QuantFin is an educational project. It is **not intended for production use** or for making real financial decisions. Use at your own risk. This library is designed for learning, experimentation, and research purposes only.

QuantFin is a lightweight Python library for working with interest-rate derivatives and curves.  
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
- SABR-style parameter fitting to market vols
- Product-specific calibration (caplets, swaptions) planned for future releases

---

## Quick Start

### Install
```
pip install -r requirements.txt
```

### Example: Bootstrapping Swap Curves
See:  
`examples/example_bootstrap.py`

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
See:  
`examples/example_bootstrap.py`

```python
ois_swap = OISSwap(3.0, 0.0023, 100)
price = ois_swap.price(ois_curve)

swap3m = Swap3M(3.0, 0.005, 100)
price = swap3m.price(ois_curve, ibor_curve)
```

### Example: Volatility Calibration
See:  
`examples/example_vol_calibration.py`

```python
from quantfin.vol.vol_surface import VolSurface

# Market data for testing
market_options = [
    { "expiry": 1.0, "strike": 100, "market_vol": 0.20, "forward": 100 },
    { "expiry": 1.0, "strike": 105, "market_vol": 0.22, "forward": 100 },
    { "expiry": 2.0, "strike": 100, "market_vol": 0.21, "forward": 100 },
    { "expiry": 2.0, "strike": 105, "market_vol": 0.23, "forward": 100 },
]

# Separate lists for the surface
expiry_list = [opt["expiry"] for opt in market_options]
strike_list = [opt["strike"] for opt in market_options]
market_vol_list = [opt["market_vol"] for opt in market_options]
forward_list = [opt["forward"] for opt in market_options]

# Create a VolSurface object
vol_surface = VolSurface(expiry_list, strike_list, market_vol_list, forward_list)

# Calibrate the model to the market vols
vol_surface.calibrate()

# Query the calibrated surface for implied vols
print("Implied vol for T=1.5, K=102, F=100:", vol_surface.get_vol(1.5, 102, 100))
print("Implied vol for T=1, K=100, F=100:", vol_surface.get_vol(1, 100, 100))
print("Implied vol for T=2, K=105, F=100:", vol_surface.get_vol(2, 105, 100))
```

---

# Future Work

Below is the recommended roadmap, broken down by module category.

---

## **1. Bootstrapping Swap Curves**
- Add interpolation for missing tenors / broken-tenor instruments during bootstrapping
- Support for more IBOR tenors, including 1m and 6m, bootstrapped using basis swaps
- Implement multiple interpolation techniques (linear, spline, monotone)

---

## **2. Volatility Calibration**
- Tests for volatility library
- Product-specific SABR calibration for:
  - Caplets
  - Swaptions
- Add logic for extrapolation

---

## **3. Risk Greeks**
- Library for calculating risk greeks for the supported instruments

---

## **4. Monte Carlo Pricing**
- Monte Carlo pricing engine to price more products generically

---

## **5. Performance and Vectorisation**
- Profile existing code for calibration/bootstrapping to see performance bottlenecks
- Use Vectorisation to accelerate calibration loops

---

## **6. Documentation and Readability**
- More details docstrings
- Improve README with diagrams of how different modules interact

---

## **7. Real Market Data Integration**
- Run against real market data pulled via APIs

---

## **8. Risk Scenarios**
- Build scenario-run functionality: shock interest rates, re-bootstrap, shock vols, etc.
- Show how these changes propagate to PnL or risk metrics

---

# Referenced Literature

---

## **1. Bootstrapping**
- Interpolation Methods for Curve Construction by Hagan
- Interest Rate Bootstrapping Explained by XAIA Investment
- A Teaching Note On Pricing and Valuing Interest Rate Swaps using LIBOR and OIS Discounting by Donald J. Smith

---

## **2. Vol Surface Calibration**
- Managing Smile Risk by Hagan
- Equivalent Black Volatilies by Hagan

---