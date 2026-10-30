import numpy as np


def pdf(m, beta, m_min, m_max):
    if isinstance(m, np.ndarray):
        magnitudes = m.copy()
    elif isinstance(m, float):
        magnitudes = np.array([m])
    else:
        raise ValueError("Wrong the magnitudes type")
    magnitudes[magnitudes < m_min] = m_min
    magnitudes[magnitudes > m_max] = m_max
    return beta * np.exp(-beta * (magnitudes - m_min)) / (1 - np.exp(-beta * (m_max - m_min)))


def cdf(m, beta, m_min, m_max):
    if isinstance(m, np.ndarray):
        magnitudes = m.copy()
    elif isinstance(m, float):
        magnitudes = np.array([m])
    else:
        raise ValueError("Wrong the magnitudes type")
    magnitudes[magnitudes < m_min] = m_min
    magnitudes[magnitudes > m_max] = m_max
    return (1 - np.exp(-beta * (magnitudes - m_min))) / (1 - np.exp(-beta * (m_max - m_min)))


def cdf_n(m, n, beta, m_min, m_max):
    return np.pow(cdf(m, beta, m_min, m_max), n)


def rnd_mag(nr_mag, beta, m_min, m_max):
    a1 = np.exp(-beta * m_min)
    a2 = np.exp(-beta * m_max)
    a12 = a1 - a2
    r = np.random.rand(nr_mag)
    mag = -np.log(a1 - r * a12) / beta
    if np.any(mag < m_min) or np.any(mag > m_max):
        raise ValueError("Magnitude out of range")
    return mag