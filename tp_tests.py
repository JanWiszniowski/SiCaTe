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
        for _ in range(nr_catalogs):  # LOOP OF CATALOGUES ===========
            mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
            m_max_obs = np.max(mag_v)
            tp_v.append(m_max_original(m_max_obs, nr_mag, beta, m_min))
            tp_iter_v.append(m_max_direct(m_max_obs, nr_mag, beta, m_min))
            m_max_obs_v.append(m_max_obs)
        tp_list.append(tp_v)
        tp_iter_list.append(tp_iter_v)
        m_max_obs_list.append(m_max_obs_v)
    return tp_list, tp_iter_list, m_max_obs_list


def test_m_max_obs(nr_mag, beta, m_min, m_max, nr_catalogs):
    m_max_obs_list = []
    for _ in range(nr_catalogs):  # LOOP OF CATALOGUES ===========
        mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
        m_max_obs = np.max(mag_v)
        m_max_obs_list.append(m_max_obs)
    return m_max_obs_list



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

def simulate_solution_existence():
    nr_catalogs = 1000
    m_max_range = (6.0, 8.5)
    m_min = 3.0
    beta = 2.3
    nr_mag_in_catalog = [v * p for p in (10, 100, 1000, 10000) for v in (10, 12, 16, 20, 25, 32, 40, 50, 63, 80)]
    print(f"nr_mag_in_catalog={nr_mag_in_catalog}")
    fig1, axis1 = plt.subplots()
    for idx, m_max in enumerate(np.linspace(m_max_range[0], m_max_range[1], num=6)):
        print(f"{idx}: m_max={m_max}")
        tp_orig_list, tp_iter_list, m_max_obs_list = test_tp(nr_mag_in_catalog, beta, m_min, m_max, nr_catalogs)
        solved_tp_iter_list = [[tp_i for tp_i in tp_iter_v if tp_i is not None] for tp_iter_v in tp_iter_list]
        solutions = [len(tp_i) / nr_catalogs for tp_i in solved_tp_iter_list]
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


def simulate_m_max_obs():
    nr_catalogs = 100
    m_max_range = (6.0, 8.5)
    m_min = 3.0
    beta = 2.3
    notch = False
    max_num = 10
    nr_mag_in_catalog = [v * p for p in (100, 1000, 10000) for v in (1, 2, 5)]
    fig, axes = plt.subplots(3, 3, gridspec_kw={'hspace': 0.25})
    m_max_list = np.linspace(m_max_range[0], m_max_range[1], num=max_num)
    m_max_texts = [f'{m_max:.1f}' for m_max in m_max_list]
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        print(f"n={nr_mag}")
        m_max_obs_lists = []
        for m_max in m_max_list:
            m_max_obs_list = test_m_max_obs(nr_mag, beta, m_min, m_max, nr_catalogs)
            m_max_obs_lists.append(m_max_obs_list)
        axis = axes[axis_index // 3, axis_index % 3]
        bplot = axis.boxplot(m_max_obs_lists, notch=notch, sym='k-', tick_labels=m_max_texts)
        m_max_beta = [m_max - 1/beta for m_max in m_max_list]
        axis.plot(range(1, max_num +1), m_max_list, color='k', linestyle='dashed', label=r'$m_{max}$')
        axis.plot(range(1, max_num +1), m_max_beta, color='gray', linestyle='dotted', label=r'$m_{max} - 1/\beta$')
        if axis_index >= 6:
            axis.set_xlabel(r"$m_{max}$", size=12)
        if axis_index % 3 == 0:
            axis.set_ylabel("$M_{max}^{obs}$", size=12)
        axis.set_title(f"{chr(97 + axis_index)}) $n(m_{{min}}={m_min})={nr_mag}$", loc='left')
        axis.legend()


if __name__ == "__main__":
    simulate_solution_existence()
    # simulate_m_max_obs()
    plt.show(block=True)
