# QuantFin

QuantFin is a lightweight Python library for **interest-rate curve construction**, **instrument pricing**, and (eventually) **volatility model calibration**.  
It is designed as an educational and extensible framework implementing modern multi-curve concepts including:

- OIS discounting
- IBOR forecasting curve
- Swap pricing
- Discount factor interpolation
- Sequential curve bootstrapping

---

## Quick Start

### Install
```
pip install -r requirements.txt
```

### Example: Bootstrapping Curves
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

### Example: Pricing Instruments  
See:  
`examples/pricing_examples.py`

```python
ois_swap = OISSwap(3.0, 0.0023, 100)
price = ois_swap.price(ois_curve)

swap3m = Swap3M(3.0, 0.005, 100)
price = swap3m.price(ois_curve, ibor_curve)
```

---

# Future Work

Below is the recommended roadmap, broken down by module category.

---

## **1. Bootstrapping Improvements**
- Add interpolation for missing tenors / broken-tenor instruments during bootstrapping
- Support for more IBOR tenors, including 1m and 6m, bootstrapped using basis swaps

---

## **2. Interpolation & Curve Methods**
- Add some sort of spline interpolation method

---

## **3. Volatility & Calibration**
- SABR calibration for:
  - Equity Options
  - Swaptions

---

# Referenced Literature

Reference for mathematics

---

## **1. Bootstrapping**
- Interpolation Methods for Curve Construction by Hagan
- Interest Rate Bootstrapping Explained by XAIA Investment
- A Teaching Note On Pricing and Valuing Interest Rate Swaps using LIBOR and OIS Discounting by Donald J. Smith

---

## **2. Vol Surface Calibration**
- Managing Smile Risk by Hagan

---