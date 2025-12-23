class NelsonSiegelDFProvider:
    def __init__(self, beta0, beta1, beta2, tau):
        self.beta0 = beta0
        self.beta1 = beta1
        self.beta2 = beta2
        self.tau = tau

    def zero_rate(self, t):
        pass

    def df(self, t):
        pass