import numpy as np

from quantfin.optimiser.base_optimiser import BaseOptimiser

# Getting around going out of bounds with NaNs/singular matrix errors
# 1. Capping on next step and finite difference bounds so we don't hit NaNs
# 2. Levenberg-Marquardt step instead of plain Gauss-Newton to avoid singular matrix errors

class SQPOptimiser(BaseOptimiser):
    def objective(self, params, residuals, args):
        # Scalar objective function used for constrained optimisation
        x = params
        expiries, strikes, forwards, market_vols = args

        residuals = residuals(x, expiries, strikes, forwards, market_vols)
        return 0.5 * np.dot(residuals, residuals)

    def gradient_objective(self, params, residuals, args):
        # Finite difference calculation of scalar objective
        x = params
        expiries, strikes, forwards, market_vols = args

        r = residuals(x, expiries, strikes, forwards, market_vols)
        J = self.jacobian(x, residuals, args)
        grad = J.T @ r

        return grad

    def solve_qp_subproblem(self, B, gradf, A, c):
        KKT = np.block([
            [B, A.T],
            [A, np.zeros((A.shape[0], A.shape[0]))]
        ])

        rhs = -np.concatenate([gradf, c])
        sol = np.linalg.solve(KKT, rhs)

        p = sol[:3]
        lam = sol[3:]

        return p, lam

    def optimise(self, x0, residuals, args, safe_params=None, constraints=None, gradient_constraints=None, max_iter=100, tol=1e-6):
        x = x0.copy()
        expiries, strikes, forwards, market_vols = args
        lam = 1e-2
        nu = 10

        for k in range(max_iter):
            f0 = self.objective(x, residuals, args)
            print(f"Iter {k}: x = {x}, f ={f0:.4f}")

            # Gradients
            grad = self.gradient_objective(x, residuals, args)

            A = gradient_constraints()[constraints(x) >= -1e-3]
            c = constraints(x)[constraints(x) >= -1e-3]

            J = self.jacobian(x, residuals, args)
            H = J.T @ J

            # empirically good step size here, can probably do better in justifying
            alpha = 0.5

            if len(A) > 0:
                # If constrained, perform KKT step
                print(f"{c} active constraint(s), performing KKT step")
                p, _ = self.solve_qp_subproblem(H, grad, A, c)

                x_new = safe_params(x + alpha * p)
                x = x_new
            else:
                # Levenberg-Marquardt step
                print("No active constraints, performing unconstrained Levenberg-Marquardt step")
                H_lm = H + lam * np.eye(len(x))
                r = residuals(x, expiries, strikes, forwards, market_vols)
                grad = J.T @ r
                p = -np.linalg.inv(H_lm) @ grad

                x_new = safe_params(x + alpha * p)
                f_new = self.objective(x_new, residuals, args)

                if f_new < f0:
                    x = x_new
                    lam /= nu
                else:
                    lam *= nu

            if np.linalg.norm(p) < 1e-8:
                break

        return x
