import numpy as np
from scipy.optimize import fsolve
import scipy.integrate as integrate
import sicate.gr as gr


class _Solver:
    def __init__(self, m_max_obs, n, beta, m_min):
        self.beta = beta
        self.n = n
        self.m_min = m_min
        self.m_max_obs = m_max_obs

    def __call__(self, m_max):
        delta = integrate.quad(gr.cdf_n, self.m_min, m_max[0], args=(self.n, self.beta, self.m_min, m_max[0]))
        fun = m_max[0] - self.m_max_obs - delta[0]
        return fun


def m_max_solve(m_max_obs, n, beta, m_min):
    delta = _Solver(m_max_obs, n, beta, m_min)
    root = fsolve(delta, np.array(m_max_obs))
    ks_condition = condition(m_max_obs, n, beta, m_min)

    if not root:
        print(f"Solver can not find the solution for the T-P estimator")
        return None
    if ks_condition:
        if root[0] >= 10.0:
            print(f"< Result {n}, {m_max_obs}, {ks_condition}, {root[0]}")
            return None
        else:
            return root[0]
    else:
        if root[0] < 10.0:
            print(f"> Result {n}, {m_max_obs}, {ks_condition}, {root[0]}")
        return None

def m_max_simple(m_max_obs, n, beta, m_min):
    delta = integrate.quad(gr.cdf_n, m_min, m_max_obs, args=(n, beta, m_min, m_max_obs))
    m_max = m_max_obs + delta
    return m_max[0]


def condition(m_max_obs, n, beta, m_min):
    return np.log(n) + 0.577 >= beta * (m_max_obs - m_min)