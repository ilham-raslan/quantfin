import math
import numpy as np

class VolModel:
    def __init__(self, alpha=0.1, rho=0, nu=0.1):
        self.alpha = alpha
        self.rho = rho
        self.nu = nu
        self.beta = 1

    def safe_params(self, x):
        return np.array([
            max(x[0], 1e-8),
            np.clip(x[1], -0.999, 0.999),
            max(x[2], 1e-8)
        ])

    def constraints(self, params):
        x = params

        alpha = x[0]
        rho = x[1]
        nu = x[2]

        return np.array([
            -alpha,
            rho - 1,
            -1 - rho,
            -nu
        ])

    # Static based on constraints
    def gradient_constraints(self):
        return np.array([
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, -1.0],
        ])

    def get_vol(self, expiry, strike, forward):
        f = forward
        k = strike
        alpha = self.alpha
        beta = self.beta
        rho = self.rho
        nu = self.nu

        if (abs(f - k)) < 1e-12:
            fk_beta  = f ** (1 - beta)
            term_1 = alpha / fk_beta
            term_2 = (1 + (((1 - beta) ** 2) / 24) * ((alpha ** 2) / (fk_beta ** 2)) + (1 / 4) * (rho * beta * alpha * nu) / fk_beta + ((2 - 3 * rho ** 2) / 24) * nu ** 2) * expiry

            return term_1 * term_2

        logFK = math.log(f / k)
        fk = f * k
        fk_beta = fk ** ((1 - beta) / 2)

        z = (nu / alpha) * fk_beta * logFK
        x = math.log((math.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))

        term_1 = alpha / (fk_beta * (1 + (((1 - beta) ** 2) / 24) * (logFK ** 2) + (((1 - beta) ** 4) / 1920) * (logFK ** 4)))
        term_2 = z / x
        term_3 = (1 + (((1 - beta) ** 2) / 24) * ((alpha ** 2) / (fk_beta ** 2)) + (1 / 4) * (rho * beta * alpha * nu) / fk_beta + ((2 - 3 * rho ** 2) / 24) * nu ** 2) * expiry

        return term_1 * term_2 * term_3
