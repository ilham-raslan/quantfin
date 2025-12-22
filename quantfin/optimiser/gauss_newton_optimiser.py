import numpy as np

from quantfin.optimiser.base_optimiser import BaseOptimiser

class GaussNewtonOptimiser(BaseOptimiser):
    def optimise(self, x0, residuals, args, safe_params=None, constraints=None, gradient_constraints=None, max_iter=100, tol=1e-6):
        x = x0[0], x0[1], x0[2]
        expiries, strikes, forwards, market_vols = args

        for k in range(max_iter):
            r = residuals(x, expiries, strikes, forwards, market_vols)
            print(f"Iter {k}: ||r|| = {np.linalg.norm(r):.4e}, x = {x}")

            J = self.jacobian(x, residuals, args)

            p = -np.linalg.inv(J.T @ J) @ (J.T @ r)

            # reduced step size of 0.5
            x_new = x + 0.5 * p
            r_new = residuals(x, expiries, strikes, forwards, market_vols)

            print(f"Iter {k}: ||r|| = {np.linalg.norm(r_new):.4e}, x = {x_new},")
            x = x_new

            if np.linalg.norm(p) < tol:
                break

        return x