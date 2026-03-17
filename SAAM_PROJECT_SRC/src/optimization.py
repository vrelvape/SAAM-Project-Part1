import numpy as np
from scipy.optimize import minimize


def compute_mv_weights(cov_matrix):
    """
    Compute long-only minimum variance portfolio weights.
    """

    n = cov_matrix.shape[0]

    # Check that covariance matrix does not contain invalid values
    if np.isnan(cov_matrix).any():
        raise ValueError("Covariance matrix contains NaN values.")

    if np.isinf(cov_matrix).any():
        raise ValueError("Covariance matrix contains infinite values.")

    def objective(w):
        return w.T @ cov_matrix @ w

    constraints = ({
        "type": "eq",
        "fun": lambda w: np.sum(w) - 1
    })

    bounds = [(0, 1)] * n
    w0 = np.ones(n) / n

    result = minimize(
        objective,
        w0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise ValueError(f"Minimum variance optimization failed: {result.message}")

    return result.x

import pandas as pd


def compute_mv_weights_by_year(
    returns_matrix,
    universe_by_year,
    rebalance_years,
    rolling_window_months,
):
    """
    Compute minimum variance portfolio weights year by year.
    """

    mv_weights_by_year = {}

    for year in rebalance_years:
        universe = universe_by_year[year]
        end = pd.Timestamp(f"{year-1}-12-31")

        # Rolling estimation window of monthly returns
        window = returns_matrix.loc[universe, :end].iloc[:, -rolling_window_months:]

        # Covariance matrix of monthly returns
        cov = window.T.cov()

        # Compute minimum variance weights
        weights = compute_mv_weights(cov.values)

        # Store weights as a pandas Series
        mv_weights_by_year[year] = pd.Series(weights, index=cov.index)

    return mv_weights_by_year