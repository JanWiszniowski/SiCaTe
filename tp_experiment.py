"""

"""
import numpy as np
from sicate.rnd import f_rnd_mag_gr
from sicate.m_max import m_max_direct_tp, m_max_original_tp
import matplotlib.pyplot as plt


def test_tp(nr_mags, beta, m_min, m_max, nr_catalogs):
    tp_list = []
    tp_iter_list = []
    m_max_obs_list = []
    for nr_mag in nr_mags:
        tp_v = []
        tp_iter_v = []
        m_max_obs_v = []
        for i_catalogs in range(nr_catalogs):  # LOOP OF CATALOGUES ===========
            mag_v = f_rnd_mag_gr(nr_mag, beta, m_min, m_max)
            m_max_obs = np.max(mag_v)
            tp_v.append(m_max_original_tp(m_max_obs, nr_mag, beta, m_min))
            tp_iter_v.append(m_max_direct_tp(m_max_obs, nr_mag, beta, m_min))
            m_max_obs_v.append(m_max_obs)
        tp_list.append(tp_v)
        tp_iter_list.append(tp_iter_v)
        m_max_obs_list.append(m_max_obs_v)
    return tp_list, tp_iter_list, m_max_obs_list


# def process(test, nr_mags, beta, m_min, m_max, nr_catalogs):
#     tp_original = []
#     tp_iter = []
#     for nr_mag in nr_mags:
#         results = test(nr_mag, beta, m_min, m_max, nr_catalogs)
#         tp_original.append(results[0])
#         tp_iter.append(results[1])
#     return tp_original, tp_iter


def boxplot(lists, tick_labels, level, level_label, title, notch=False):
    figure, axis = plt.subplots()
    axis.set_title(title)
    axis.boxplot(lists, notch=notch, sym='k.', tick_labels=tick_labels,
                 flierprops=dict(markersize=2))
    axis.hlines(level, 0, len(lists) + 1, colors=None, linestyles='dotted', label=level_label)
    axis.tick_params("x", rotation=75)
    axis.legend()


def pointplot(x, y, xy_label, level, level_label, title):
    figure, axis = plt.subplots()
    axis.set_title(title)
    axis.plot(x, y, 'o', label=xy_label)
    axis.hlines(level, x[0], x[-1], linestyles='dotted', label=level_label)
    axis.legend()


def main():
    nr_catalogs = 10000
    m_max = 6.5
    m_min = 3.0
    beta = 2.3
    notch = False
    nr_mag_in_catalog = range(1000, 20001, 1000)
    tp_orig_list, tp_iter_list, m_max_obs_list = test_tp(nr_mag_in_catalog, beta, m_min, m_max, nr_catalogs)
    solved_tp_iter_list = [[tp_i for tp_i in tp_iter_v if tp_i is not None] for tp_iter_v in tp_iter_list]
    solved_delta_list = [[tp_i1 - tp_i2 for tp_i1, tp_i2 in zip(tp_iter_v, m_max_obs_v) if tp_i1 is not None]
                         for tp_iter_v, m_max_obs_v in zip(tp_iter_list, m_max_obs_list)]
    solved_m_max_obs_list = [[tp_i2 for tp_i1, tp_i2 in zip(tp_iter_v, m_max_obs_v) if tp_i1 is not None]
                             for tp_iter_v, m_max_obs_v in zip(tp_iter_list, m_max_obs_list)]
    solved_tp_orig_list = [[tp_i2 for tp_i1, tp_i2 in zip(tp_iter_v, tp_orig_v) if tp_i1 is not None]
                           for tp_iter_v, tp_orig_v in zip(tp_iter_list, tp_orig_list)]
    solutions = [len(tp_i) / nr_catalogs for tp_i in solved_tp_iter_list]
    tick_labels = [str(nr_mag) for nr_mag in nr_mag_in_catalog]
    #
    pointplot(nr_mag_in_catalog, solutions, 'solution ratio', 0.95,
              'p = 0.05', "Direct T-P estimator solution ratio")

    boxplot(m_max_obs_list, tick_labels, m_max, '$m_{max}$',
            "$m_{max}^{obs}$", notch=notch)
    boxplot(solved_m_max_obs_list, tick_labels, m_max, '$m_{max}$',
            "$m_{max}^{obs}$ for allowed solutions", notch=notch)
    boxplot(solved_tp_iter_list, tick_labels, m_max, '$m_{max}$',
            "$m_{max}$ of direct T-P estimator", notch=notch)
    boxplot(tp_orig_list, tick_labels, m_max, '$m_{max}$',
            "$m_{max}$ of original T-P estimator for all solutions", notch=notch)
    boxplot(solved_tp_orig_list, tick_labels, m_max, '$m_{max}$',
            "$m_{max}$ of original T-P estimator for allowed solutions", notch=notch)
    boxplot(solved_delta_list, tick_labels, 1 / beta, r'$1/\beta$',
            r"$\Delta$ values", notch=notch)
    plt.show(block=True)


if __name__ == "__main__":
    main()
