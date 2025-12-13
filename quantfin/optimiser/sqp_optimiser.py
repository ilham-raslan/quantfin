import numpy as np

from quantfin.optimiser.base_optimiser import BaseOptimiser

# Getting around going out of bounds with NaNs
# 1. Capping finite difference bounds so we don't hit NaNs
# 2. BFGS update can divide by 0, so skip it if denominator is too small
# 3. KKT system can be singular, so regularise it

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
            alpha,
            rho - 1,
            -1 - rho,
            nu
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
        B_reg = B + 1e-8 * np.eye(3)
        KKT = np.block([
            [B_reg, A.T],
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
        x = x0.copy()
        lam = np.zeros(1)
        B = np.eye(3)

        for k in range(max_iter):
            print(f"Iter {k}: x = {x}, f ={self.objective(x):.4f}")

            # Gradients
            grad = self.gradient_objective(x)

            A = self.gradient_constraints()[self.constraints(x) >= -1e-8]
            c = self.constraints(x)[self.constraints(x) >= -1e-8]

            if len(A) > 0:
                p, lam_new = self.solve_qp_subproblem(B, grad, A, c)
            else:
                p = -np.linalg.solve(B, grad)
                lam_new = np.zeros(0)

            x_new = x + p

            # BFGS update for B
            s = p
            y = self.gradient_objective(x_new) - self.gradient_objective(x)
            ys = y @ s

            # Want to ensure denominator isn't too small
            if ys > 1e-10 and s @ B @ s > 1e-10:
                B = B + np.outer(y, y) / ys - (B @ np.outer(s, s) @ B) / (s @ B @ s)

            x = x_new
            lam = lam_new

            if np.linalg.norm(p) < 1e-8:
                break

        return x, lam
