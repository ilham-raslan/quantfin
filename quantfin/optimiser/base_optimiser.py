import numpy as np

class BaseOptimiser:
    def __init__(self, residuals, expiries, strikes, market_vols, forwards):
        self.residuals = residuals
        self.expiries = expiries
        self.strikes = strikes
        self.market_vols = market_vols
        self.forwards = forwards

    # Clamp off params during FD, otherwise we go out of bounds
    def safe_params(self, x):
        return np.array([
            max(x[0], 1e-8),
            np.clip(x[1], -0.999, 0.999),
            max(x[2], 1e-8)
        ])

    def jacobian(self, params):
        # Finite difference calculation of the jacobians
        x = params
        base_residuals = self.residuals(x, self.expiries, self.strikes, self.forwards, self.market_vols)
        # bump alpha up by 0.01
        alpha_up_x = self.safe_params((x[0] + 0.01, x[1], x[2]))
        alpha_up_residuals = self.residuals(alpha_up_x, self.expiries, self.strikes, self.forwards, self.market_vols)

        rho_up_x = self.safe_params((x[0], x[1] + 0.01, x[2]))
        rho_up_residuals = self.residuals(rho_up_x, self.expiries, self.strikes, self.forwards, self.market_vols)

        nu_up_x = self.safe_params((x[0], x[1], x[2] + 0.01))
        nu_up_residuals = self.residuals(nu_up_x, self.expiries, self.strikes, self.forwards, self.market_vols)

        data_points = len(self.expiries)
        alpha_deltas = (alpha_up_residuals - base_residuals) / 0.01
        rho_deltas = (rho_up_residuals - base_residuals) / 0.01
        nu_deltas = (nu_up_residuals - base_residuals) / 0.01

        jacobian = np.hstack((alpha_deltas.reshape(data_points, 1), rho_deltas.reshape(data_points, 1), nu_deltas.reshape(data_points, 1)))

        return jacobian

    def optimise(self, x0, max_iter=100, tol=1e-6):
        raise NotImplementedError