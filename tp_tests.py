"""

"""
import numpy as np
import sicate.gr as gr
from sicate.tp import m_max_direct, m_max_original
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
            mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
            m_max_obs = np.max(mag_v)
            tp_v.append(m_max_original(m_max_obs, nr_mag, beta, m_min))
            tp_iter_v.append(m_max_direct(m_max_obs, nr_mag, beta, m_min))
            m_max_obs_v.append(m_max_obs)
        tp_list.append(tp_v)
        tp_iter_list.append(tp_iter_v)
        m_max_obs_list.append(m_max_obs_v)
    return tp_list, tp_iter_list, m_max_obs_list


def boxplot(lists, tick_labels, level, level_label, title, notch=False):
    figure, axis = plt.subplots()
    axis.set_title(title)
    axis.boxplot(lists, notch=notch, sym='k.', tick_labels=tick_labels,
                 flierprops=dict(markersize=2))
    axis.hlines(level, 0, len(lists) + 1, colors=None, linestyles='dotted', label=level_label)
    axis.tick_params("x", rotation=75)
    axis.legend()


def plot_points(x, y, axis=None, idx=None, m_max=None):
    colors = plt.cm.tab10
    markers = ['o', 'v', '^', 's', 'd', '>', '<', '+', 'x', '*']
    if axis is None:
        figure, axis = plt.subplots()
    m_max_text = r"m_{max}"
    if idx is None:
        color = 'k'
        marker = 'o'
    else:
        color = colors.colors[idx]
        marker = markers[idx]
    if m_max is None:
        label_text = None
    else:
        label_text = f"${m_max_text}={m_max:.1f}$"
    axis.semilogx(x, y, color=color, label=label_text, marker=marker, markersize=6)

def main():
    nr_catalogs = 1000
    m_max_range = (6.0, 8.5)
    m_max_step = 0.2
    m_min = 3.0
    beta = 2.3
    notch = False
    nr_mag_in_catalog = [v * p for p in (100, 1000, 10000, 100000) for v in (1, 2, 5)]
    fig1, axis1 = plt.subplots()
    for idx, m_max in enumerate(np.linspace(m_max_range[0], m_max_range[1], num=6)):
        print(f"{idx}: m_max={m_max}")
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
        plot_points(nr_mag_in_catalog, solutions, axis=axis1, idx=idx, m_max=m_max)
    axis1.hlines(0.95, nr_mag_in_catalog[0], nr_mag_in_catalog[-1], linestyles='dotted', label=r'$\alpha = 0.05$')
    axis1.set_title("Direct T-P estimator solution ratio")
    axis1.set_xlim(nr_mag_in_catalog[0] / 1.1, nr_mag_in_catalog[-1] * 1.1)
    axis1.set_xlabel('n')
    axis1.legend()

    # boxplot(m_max_obs_list, tick_labels, m_max, '$m_{max}$',
    #         "$m_{max}^{obs}$", notch=notch)
    # boxplot(solved_m_max_obs_list, tick_labels, m_max, '$m_{max}$',
    #         "$m_{max}^{obs}$ for allowed solutions", notch=notch)
    # boxplot(solved_tp_iter_list, tick_labels, m_max, '$m_{max}$',
    #         "$m_{max}$ of direct T-P estimator", notch=notch)
    # boxplot(tp_orig_list, tick_labels, m_max, '$m_{max}$',
    #         "$m_{max}$ of original T-P estimator for all solutions", notch=notch)
    # boxplot(solved_tp_orig_list, tick_labels, m_max, '$m_{max}$',
    #         "$m_{max}$ of original T-P estimator for allowed solutions", notch=notch)
    # boxplot(solved_delta_list, tick_labels, 1 / beta, r'$1/\beta$',
    #         r"$\Delta$ values", notch=notch)
    plt.show(block=True)


if __name__ == "__main__":
    main()
