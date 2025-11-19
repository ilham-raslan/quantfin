from quantfin.curves.ibor_curve import IBORCurve3M
from quantfin.curves.ois_curve import OISCurve

class MultiCurveBootstrapper:
    def __init__(self, ois_swaps, swaps3m):
        self.ois_swaps = ois_swaps
        self.swaps3m = swaps3m

    def bootstrap_ois(self):
        times = [0.0]
        dfs = [1.0]
        ois_curve = OISCurve()

        for i, swap in enumerate(self.ois_swaps):
            k = sum(0.25 * swap.fixed_rate * ois_curve.df(t) for t in times[1:])
            df = (1 - k) / (0.25 * swap.fixed_rate + 1)

            times.append(swap.maturity)
            dfs.append(df)
            ois_curve.add_knot(swap.maturity, df)

        return ois_curve

    def bootstrap_ibor3m(self, ois_curve):
        times = [0.0]
        dfs = [1.0]
        ibor3m_curve = IBORCurve3M(ois_curve)
        for i, swap in enumerate(self.swaps3m):
            fixed_leg_pv = swap.fixed_rate * sum(0.25 * ois_curve.df(swap.maturity) for _ in times + [swap.maturity])
            k = sum(ois_curve.df(time) * (dfs[j - 1] / dfs[j] - 1) for j, (time, df) in enumerate(zip(times, dfs)))
            df = dfs[i] * ois_curve.df(times[i]) / (dfs[i] + fixed_leg_pv + k)

            times.append(swap.maturity)
            dfs.append(df)

            ibor3m_curve.add_knot(swap.maturity, df)

        return ibor3m_curve

    def fit(self):
        ois_curve = self.bootstrap_ois()
        ibor_3m_curve = self.bootstrap_ibor3m(ois_curve)

        return {
            "ois" : ois_curve,
            "3m" : ibor_3m_curve
        }
