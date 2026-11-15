import numpy as np
import sicate.gr as gr
import matplotlib.pyplot as plt


EPS = np.finfo(float).eps


def test_m_max_obs(nr_mag, beta, m_min, m_max, nr_catalogs):
    m_max_obs_list = []
    for _ in range(nr_catalogs):  # LOOP OF CATALOGUES ===========
        mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
        m_max_obs = np.max(mag_v)
        m_max_obs_list.append(m_max_obs)
    return m_max_obs_list


def simulate_m_max_obs():
    nr_catalogs = 10000
    m_max_range = (6.0, 8.5)
    m_min = 3.0
    beta = 2.3
    notch = False
    max_num = 10
    nr_mag_in_catalog = [v * p for p in (100, 1000, 10000) for v in (1, 2, 5)]
    fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, gridspec_kw={'hspace': 0.15, "wspace": 0.02},
                             figsize=(12.0, 10.0))
    m_max_list = np.linspace(m_max_range[0], m_max_range[1], num=max_num)
    m_max_texts = [f'{m_max:.1f}' for m_max in m_max_list]
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        print(f"n={nr_mag}")
        m_max_obs_lists = []
        for m_max in m_max_list:
            m_max_obs_list = test_m_max_obs(nr_mag, beta, m_min, m_max, nr_catalogs)
            m_max_obs_lists.append(m_max_obs_list)
        axis = axes[axis_index // 3, axis_index % 3]
        axis.boxplot(m_max_obs_lists, notch=notch, tick_labels=m_max_texts,
                     flierprops=dict(marker='o', markerfacecolor='lightgray', markersize=1, markeredgecolor='none'))
        m_max_beta = [m_max - 1 / beta for m_max in m_max_list]
        axis.plot(range(1, max_num + 1), m_max_list, color='gray', linestyle='dashed', label=r'$m_{max}$')
        axis.plot(range(1, max_num + 1), m_max_beta, color='gray', linestyle='dotted', label=r'$m_{max} - 1/\beta$')
        if axis_index >= 6:
            axis.set_xlabel(r"$m_{max}$", size=12)
        if axis_index % 3 == 0:
            axis.set_ylabel("$m_{max}^{obs}$", size=12)
        axis.set_title(f"{chr(97 + axis_index)}) $n(m_{{c}}={m_min})={nr_mag}$", loc='left')
        axis.legend()


def plot_one_boxplot(axes, axis_index, lists, m_max_list, m_min, nr_mag, notch=False):
    max_num = len(m_max_list)
    m_max_texts = [f'{m_max:.1f}' for m_max in m_max_list]
    axis = axes[axis_index // 3, axis_index % 3]
    axis.boxplot(lists, notch=notch, tick_labels=m_max_texts,
                 flierprops=dict(marker='o', markerfacecolor='lightgray', markersize=1, markeredgecolor='none'))
    if axis_index >= 6:
        axis.set_xlabel(r"$m_{max}$", size=12)
    if axis_index % 3 == 0:
        axis.set_ylabel(r"$\hat{m}_{max}$", size=12)
    axis.set_title(f"{chr(97 + axis_index)}) $n(m_{{c}}={m_min})={nr_mag}$", loc='left')
    axis.plot(range(1, max_num + 1), m_max_list, color='gray', linestyle='dashed', label=r'$\hat{m}_{max}=m_{max}$')
    axis.legend()


def boxplot(lists, tick_labels, level, level_label, title, notch=False):
    figure, axis = plt.subplots()
    axis.set_title(title)
    axis.boxplot(lists, notch=notch, tick_labels=tick_labels,
                 flierprops=dict(marker='o', markerfacecolor='lightgray', markersize=1, markeredgecolor='none'))
    axis.hlines(level, 0, len(lists) + 1, colors=None, linestyles='dotted', label=level_label)
    axis.tick_params("x", rotation=75)
    axis.legend()


def plot_points_n(x, y, axis=None, idx=None, m_max=None):
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


if __name__ == "__main__":
    simulate_m_max_obs()
    plt.show(block=True)
