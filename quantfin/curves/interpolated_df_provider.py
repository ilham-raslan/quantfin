class InterpolateDFProvider:
    def __init__(self, times, dfs, interpolator):
        self.times = times
        self.dfs = dfs
        self.interpolator = interpolator(times, dfs)

    def df(self, t):
        return self.interpolator(t)