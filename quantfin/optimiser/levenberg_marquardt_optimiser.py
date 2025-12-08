import numpy as np

from quantfin.optimiser.base_optimiser import BaseOptimiser

class LevenbergMarquardtOptimiser(BaseOptimiser):
    def optimise(self, x0, max_iter=100, tol=1e-6):
        x = x0[0], x0[1], x0[2]
        lam = 1e-3
        nu = 10

        for k in range(max_iter):
            r = self.residuals(x, self.expiries, self.strikes, self.forwards, self.market_vols)
            print(f"Iter {k}: ||r|| = {np.linalg.norm(r):.4e}, x = {x}")

            J = self.jacobian(x)

            p = -(np.linalg.inv(J.T @ J + lam * np.eye(len(x)))) @ (J.T @ r)

            # reduced step size of 0.1
            x_new = x + 0.1 * p
            r_new = self.residuals(x_new, self.expiries, self.strikes, self.forwards, self.market_vols)

            if np.linalg.norm(r_new) < np.linalg.norm(r):
                x = x_new
                lam /= nu
            else:
                lam *= nu

            if np.linalg.norm(p) < tol:
                break

        return x