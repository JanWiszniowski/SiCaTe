import numpy as np


def f_pdf_gr(m, beta, m_min, m_max):
    if isinstance(m, np.ndarray):
        magnitudes = m.copy()
    elif isinstance(m, float):
        magnitudes = np.array([m])
    else:
        raise ValueError("Wrong the magnitudes type")
    magnitudes[magnitudes < m_min] = m_min
    magnitudes[magnitudes > m_max] = m_max
    return beta * np.exp(-beta * (magnitudes - m_min)) / (1 - np.exp(-beta * (m_max - m_min)))
