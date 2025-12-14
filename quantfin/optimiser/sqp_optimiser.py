import numpy as np

from quantfin.optimiser.base_optimiser import BaseOptimiser

# Getting around going out of bounds with NaNs/singular matrix errors
# 1. BFGS update can divide by 0, so skip it if denominator is too small
# 2. Capping on next step and finite difference bounds so we don't hit NaNs
# 3. Levenberg-Marquardt step instead of plain Gauss-Newton to avoid singular matrix errors

class SQPOptimiser(BaseOptimiser):
    def objective(self, params):
        # Scalar objective function used for constrained optimisation
        x = params
        residuals = self.residuals(x, self.expiries, self.strikes, self.forwards, self.market_vols)
        return 0.5 * np.dot(residuals, residuals)

    def gradient_objective(self, params):
        # Finite difference calculation of scalar objective
        x = params

        r = self.residuals(x, self.expiries, self.strikes, self.forwards, self.market_vols)
        J = self.jacobian(x)
        grad = J.T @ r

        return grad

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
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1],
        ])

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

    # Clamp off params during FD, otherwise we go out of bounds
    def safe_params(self, x):
        return np.array([
            max(x[0], 1e-3),
            np.clip(x[1], -0.9999, 0.9999),
            max(x[2], 1e-3)
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
        x = x0.copy()
        B = np.eye(3)
        lam = 1e-2
        nu = 10

        for k in range(max_iter):
            f0 = self.objective(x)
            print(f"Iter {k}: x = {x}, f ={f0:.4f}")

            # Gradients
            grad = self.gradient_objective(x)

            A = self.gradient_constraints()[self.constraints(x) >= -1e-3]
            c = self.constraints(x)[self.constraints(x) >= -1e-3]

            if len(A) > 0:
                # If constrained, perform KKT step
                print(f"{c} active constraint(s), performing KKT step")
                p, _ = self.solve_qp_subproblem(B, grad, A, c)

                x_new = self.safe_params(x + p)
            else:
                # Levenberg-Marquardt step
                print("No active constraints, performing unconstrained Levenberg-Marquardt step")
                J = self.jacobian(x)
                r = self.residuals(x, self.expiries, self.strikes, self.forwards, self.market_vols)
                H = J.T @ J
                H_lm = H + lam + np.eye(len(x))
                grad = J.T @ r
                p = -np.linalg.inv(H_lm) @ grad

                x_new = self.safe_params(x + p)
                f_new = self.objective(x_new)

                if f_new < f0:
                    x = x_new
                    lam /= nu
                else:
                    lam *= nu

            # BFGS update for B
            s = p
            y = self.gradient_objective(x_new) - self.gradient_objective(x)
            ys = y @ s

            # Want to ensure denominator isn't too small
            if ys > 1e-10 and s @ B @ s > 1e-10:
                B = B + np.outer(y, y) / ys - (B @ np.outer(s, s) @ B) / (s @ B @ s)

            if np.linalg.norm(p) < 1e-8:
                break

        return x
