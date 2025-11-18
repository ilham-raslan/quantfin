class OISCurve:
    def __init__(self):
        self.times = [0]
        self.df = [1]

    def add_knot(self, t, df):
        self.times.append(t)
        self.df.append(df)

    def df(self, t):
        pass

    def zero_rate(self, t):
        pass
