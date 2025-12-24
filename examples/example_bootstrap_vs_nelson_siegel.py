from examples.data.markets import OIS_FUTURES, OIS_SWAPS, SWAPS_3M
from quantfin.curves.curve_manager import CurveManager
import numpy as np
import matplotlib.pyplot as plt

ois_futures = OIS_FUTURES
ois_swaps = OIS_SWAPS
swaps_3m = SWAPS_3M

ois_instruments = ois_futures + ois_swaps

curve_manager = CurveManager()
bootstrapped_curves = curve_manager.build(ois_instruments, swaps_3m, model="log_linear_bootstrapped")
nelson_siegel_curves = curve_manager.build(ois_instruments, swaps_3m, model="nelson_siegel", calibration_engine="levenberg_marquardt")

bootstrapped_ois_curve = bootstrapped_curves["ois"]
bootstrapped_3m_curve = bootstrapped_curves["3m"]
nelson_siegel_ois_curve = nelson_siegel_curves["ois"]
nelson_siegel_3m_curve = nelson_siegel_curves["3m"]

t_values = np.arange(0, 5.25, 0.25)

bootstrapped_ois_dfs = [bootstrapped_ois_curve.df(t) for t in t_values]
bootstrapped_3m_forward_rates = [bootstrapped_3m_curve.forward_rate(t_values[i], t_values[i + 1]) for i in range(len(t_values) - 1)]
nelson_siegel_ois_dfs = [nelson_siegel_ois_curve.df(t) for t in t_values]
nelson_siegel_3m_forward_rates = [nelson_siegel_3m_curve.forward_rate(t_values[i], t_values[i + 1]) for i in range(len(t_values) - 1)]

# Compare discount factors
plt.figure(figsize=(10, 5))
plt.plot(t_values, bootstrapped_ois_dfs, marker="o", label="Bootstrapped OIS discount factors")
plt.plot(t_values, nelson_siegel_ois_dfs, marker="*", label="Nelson Siegel OIS discount factors")
plt.title("Discount Factors vs time")
plt.xlabel("Time (Years)")
plt.ylabel("Discount Factor")
plt.grid(True)
plt.legend()
plt.show()

# Compare 3m forward rates
plt.figure(figsize=(10, 5))
plt.plot(t_values[:-1], bootstrapped_3m_forward_rates, marker="o", label="Bootstrapped 3m forward rates")
plt.plot(t_values[:-1], nelson_siegel_3m_forward_rates, marker="*", label="Nelson Siegel 3m forward rates")
plt.title("3m Forward Rates vs time")
plt.xlabel("Time (Years)")
plt.ylabel("3m Forward Rate")
plt.grid(True)
plt.legend()
plt.show()