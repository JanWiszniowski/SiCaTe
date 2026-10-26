import numpy as np
from sicate.pdf import f_pdf_gr
from scipy.optimize import fsolve
from scipy.special import lambertw


class TPSolver:
    def __init__(self, m_max_obs, beta, n, m_min):
        self.beta = beta
        self.n = n
        self.m_min = m_min
        self.m_max_obs = m_max_obs

    def __call__(self, m_max):
        fun = m_max - self.m_max_obs - 1.0 / (self.n * f_pdf_gr(m_max, self.beta, self.m_min, m_max))
        return fun


def _m_max_equation_to_solve(x, m_max_obs, beta, n, m_min):
    fun = x - m_max_obs - 1.0 / (n * f_pdf_gr(x, beta, m_min, x))
    return fun


def tp_condition(n, beta, m_min, m_max_obs):
    return np.log(n) - (n - 1) / n >= beta * (m_max_obs - m_min)


# def tp_condition(n, beta, m_min, m_max_obs):
#     return np.log(n) >= beta * (m_max_obs - m_min) + 1


# def tp_condition(n, beta, m_min, m_max_obs):
#     return np.exp(1) * np.exp(beta * (m_max_obs - m_min) - 1 / n) <= n


def m_max_direct_tp(m_max_obs, n, beta, m_min):
    if tp_condition(n, beta, m_min, m_max_obs):
        w = lambertw(-np.exp(beta * (m_max_obs - m_min) - 1 / n) / n)
        if w.imag != 0.0:
            raise ValueError(f"Imag nonzero: {w.imag} {-np.exp(beta * (m_max_obs - m_min) + 1 / n) / n} {-1/np.exp(1)}")
        delta = - w.real / beta - 1 / (n * beta)
        # print(f"Delta {delta}, {w.real}, {n}")
        m_max = m_max_obs + delta
        return m_max
    else:
        w = lambertw(-np.exp(beta * (m_max_obs - m_min) + 1 / n) / n)
        if w.imag == 0.0:
            raise ValueError(f"Imag zero")
        return None


def m_max_tp(m_max_obs, n, beta, m_min):
    # delta = TPSolver(m_max_obs, beta, n, m_min)
    # root = fsolve(delta, np.array(m_max_obs))
    root = fsolve(_m_max_equation_to_solve, np.array(m_max_obs), args=(m_max_obs, beta, n, m_min))
    print(f"Result {n}, {m_max_obs}, {tp_condition(n, beta, m_min, m_max_obs)}, {root}")
    if not root:
        print(f"Solver can not find the solution for the T-P estimator")
        return None
    if len(root) > 1:
        return np.min(root)
    else:
        return root[0]


def m_max_iter_tp(m_max_obs, n, beta, m_min, accuracy=0.1):
    a1 = np.exp(-beta * m_min)
    m_max_est_old = 0
    m_max_est_new = m_max_obs
    nr_iter_max = 10
    nr_iter = 0
    print(f"{np.log(n) - beta * (m_max_obs - m_min) - (n - 1) / n}")
    if not tp_condition(n, beta, m_min, m_max_obs):
        print(f"nop solution")
        print(f"{m_max_direct_tp(m_max_obs, n, beta, m_min)}")
    else:
        print(f"ok solution")
        print(f"Direct {m_max_direct_tp(m_max_obs, n, beta, m_min)}")
    while (abs(m_max_est_new - m_max_est_old) > accuracy) and (nr_iter < nr_iter_max):
        nr_iter = nr_iter + 1
        m_max_est_old = m_max_est_new
        a2_current = np.exp(-beta * m_max_est_old)  # a2  (ESTIMATED)
        a12_current = a1 - a2_current  # a12 (ESTIMATED)
        f = beta * a2_current / a12_current
        if f > 0:
            m_max_est_new = m_max_obs + 1 / (n * f)
        else:
            nr_iter = nr_iter_max
    print(f"Result {n}, {m_max_obs}, {tp_condition(n, beta, m_min, m_max_obs)}, {m_max_est_new}")
    if nr_iter == nr_iter_max or m_max_est_new > 20.0:
        print(f"Solver can not find the solution for the T-P estimator {n}, {tp_condition(n, beta, m_min, m_max_obs)}")
        return None
    return m_max_est_new


def m_max_original_tp(m_max_obs, n, beta, m_min):
    m_max = m_max_obs + 1.0 / (n * f_pdf_gr(m_max_obs, beta, m_min, m_max_obs))
    return m_max[0]