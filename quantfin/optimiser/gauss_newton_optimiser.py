import numpy as np

class GaussNewtonOptimiser:
    def __init__(self, residuals, expiries, strikes, market_vols, forwards):
        self.residuals = residuals
        self.expiries = expiries
        self.strikes = strikes
        self.market_vols = market_vols
        self.forwards = forwards

    # TODO: Clean params up, actually used passed in params
    def jacobian(self, params, expiries, strikes, forwards, market_vols):
        # Finite difference calculation of the jacobians
        x = params
        base_residuals = self.residuals(x, self.expiries, self.strikes, self.forwards, self.market_vols)
        # bump alpha up by 0.01
        alpha_up_x = x[0] + 0.01, x[1], x[2]
        alpha_up_residuals = self.residuals(alpha_up_x, self.expiries, self.strikes, self.forwards, self.market_vols)

        rho_up_x = x[0], x[1] + 0.01, x[2]
        rho_up_residuals = self.residuals(rho_up_x, self.expiries, self.strikes, self.forwards, self.market_vols)

        nu_up_x = x[0], x[1], x[2] + 0.01
        nu_up_residuals = self.residuals(nu_up_x, self.expiries, self.strikes, self.forwards, self.market_vols)

        data_points = len(self.expiries)
        alpha_deltas = (alpha_up_residuals - base_residuals) / 0.01
        rho_deltas = (rho_up_residuals - base_residuals) / 0.01
        nu_deltas = (nu_up_residuals - base_residuals) / 0.01

        jacobian = np.hstack((alpha_deltas.reshape(data_points, 1), rho_deltas.reshape(data_points, 1), nu_deltas.reshape(data_points, 1)))

        return jacobian

    def optimise(self, x0, max_iter=20, tol=1e-6):
        x = x0[0], x0[1], x0[2]

        for k in range(max_iter):
            r = self.residuals(x, self.expiries, self.strikes, self.forwards, self.market_vols)
            print(f"Iter {k}: ||r|| = {np.linalg.norm(r):.4e}, x = {x}")

            J = self.jacobian(x, self.expiries, self.strikes, self.forwards, self.market_vols)

            p = -np.linalg.inv(J.T @ J) @ (J.T @ r)

            # reduced step size of 0.1
            x_new = x + 0.1 * p
            r_new = self.residuals(x, self.expiries, self.strikes, self.forwards, self.market_vols)

            print(f"Iter {k}: ||r|| = {np.linalg.norm(r_new):.4e}, x = {x_new},")
            x = x_new

            if np.linalg.norm(p) < tol:
                break

        return x