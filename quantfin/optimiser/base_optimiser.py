import numpy as np

class BaseOptimiser:

    def jacobian(self, x, residuals, args, safe_params=None):
        if safe_params is None:
            def safe_params(y):
                return y

        data_points = len(args[0]) if isinstance(args, tuple) else len(args)

        # Finite difference calculation of the jacobians
        base_residuals = residuals(x, *args)

        up_bumps = [safe_params([x[j] + 0.01 if i == j else x[j] for j in range(len(x))]) for i in range(len(x))]
        up_bumps_residuals = [residuals(param, *args) for param in up_bumps]
        deltas = [(up_bump_residuals - base_residuals) / 0.01 for up_bump_residuals in up_bumps_residuals]

        jacobian = np.hstack([delta.reshape(data_points, 1) for delta in deltas])

        return jacobian

    def optimise(self, x0, residuals, args, safe_params=None, constraints=None, gradient_constraints=None, max_iter=100, tol=1e-6):
        pass