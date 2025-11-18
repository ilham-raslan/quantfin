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
            fixed_leg_pv = 0.0
            if i > 0:
                for j in range(1, len(times)):
                    delta = times[j] - times[j - 1]
                    fixed_leg_pv += swap.fixed_rate * delta * dfs[j]

            prev_maturity = times[-1]
            delta = swap.maturity - prev_maturity
            df = (1 - fixed_leg_pv) / (1 + swap.fixed_rate * delta)

            times.append(swap.maturity)
            dfs.append(df)
            ois_curve.add_knot(swap.maturity, df)

        return ois_curve

    def bootstrap_ibor3m(self, ois_curve):
        pass

    def fit(self):
        pass
