import numpy as np

class BaseOptimiser:

    def jacobian(self, x, residuals, args, safe_params=None):
        if safe_params is None:
            def safe_params(y):
                return y

        expiries, strikes, forwards, market_vols = args

        # Finite difference calculation of the jacobians
        base_residuals = residuals(x, expiries, strikes, forwards, market_vols)
        # bump alpha up by 0.01
        alpha_up_x = safe_params((x[0] + 0.01, x[1], x[2]))
        alpha_up_residuals = residuals(alpha_up_x, expiries, strikes, forwards, market_vols)

        rho_up_x = safe_params((x[0], x[1] + 0.01, x[2]))
        rho_up_residuals = residuals(rho_up_x, expiries, strikes, forwards, market_vols)

        nu_up_x = safe_params((x[0], x[1], x[2] + 0.01))
        nu_up_residuals = residuals(nu_up_x, expiries, strikes, forwards, market_vols)

        data_points = len(args[0])
        alpha_deltas = (alpha_up_residuals - base_residuals) / 0.01
        rho_deltas = (rho_up_residuals - base_residuals) / 0.01
        nu_deltas = (nu_up_residuals - base_residuals) / 0.01

        jacobian = np.hstack((alpha_deltas.reshape(data_points, 1), rho_deltas.reshape(data_points, 1), nu_deltas.reshape(data_points, 1)))

        return jacobian

    def optimise(self, x0, residuals, args, safe_params=None, constraints=None, gradient_constraints=None, max_iter=100, tol=1e-6):
        pass