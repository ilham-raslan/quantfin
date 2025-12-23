from quantfin.bootstrap.bootstrapper import MultiCurveBootstrapper


class CurveManager:
    def build(self, ois_swaps, swaps3m, mode="bootstrap"):
        if mode == "bootstrap":
            bootstrapper = MultiCurveBootstrapper(ois_swaps, swaps3m)
            curves = bootstrapper.fit()

            return {
                "ois": curves["ois"],
                "3m": curves["3m"]
            }
        else:
            raise ValueError(f"Curve build mode {mode} is not supported")