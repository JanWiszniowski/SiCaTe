import numpy as np


def f_rnd_mag_gr(nr_mag, beta, m_min, m_max):
    a1 = np.exp(-beta * m_min)
    a2 = np.exp(-beta * m_max)
    a12 = a1 - a2
    r = np.random.rand(nr_mag)
    mag = -np.log(a1 - r * a12) / beta
    if np.any(mag < m_min) or np.any(mag > m_max):
        raise ValueError("Magnitude out of range")
    return mag,