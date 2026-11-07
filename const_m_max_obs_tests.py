import numpy as np
import sicate.gr as gr
from sicate.tp import m_max_direct, m_max_original
import matplotlib.pyplot as plt


def rnd_m_max(nr_mag, beta, m_min, m_max_range, nr_catalogs):
    m_max_obs_dict = {}
    for i_catalogs in range(nr_catalogs):
        m_max = np.random.rand() * (m_max_range[1] - m_max_range[0]) + m_max_range[0]
        # print(m_max)
        mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
        m_max_obs = np.max(mag_v)
        if m_max_obs > m_max:
            print(f"{m_max_obs} > {m_max}")
        d_m_max_obs = round(m_max_obs * 5) / 5
        # m_max_obs = np.round(np.max(mag_v), decimals=1)
        if d_m_max_obs not in m_max_obs_dict:
            m_max_obs_dict[d_m_max_obs] = {'m_max': [], 'm_max_direct': [], 'm_max_original': [],
                                           'm_max_obs': []}
        m_max_obs_dict[d_m_max_obs]['m_max_original'].append(m_max_original(m_max_obs, nr_mag, beta, m_min))
        m_max_obs_dict[d_m_max_obs]['m_max_direct'].append(m_max_direct(m_max_obs, nr_mag, beta, m_min))
        m_max_obs_dict[d_m_max_obs]['m_max'].append(m_max)
        m_max_obs_dict[d_m_max_obs]['m_max_obs'].append(m_max_obs)
    return m_max_obs_dict


def boxplot_m_max_obs(init_obs_list, init_lists, title, corected=1000, level=None, level_label=None,
                      notch=False, axis=None):
    if axis is None:
        figure, axis = plt.subplots()
    axis.set_title(title, loc='left')
    # colors = ['k' if idx < corected else 'm' for idx in range(len(lists))]
    begin_list = 0
    while len(init_lists[begin_list]) < 20:
        begin_list += 1
    lists = init_lists[begin_list:]
    len_lists = len(lists)
    m_max_obs_list = init_obs_list[begin_list:begin_list + len_lists]
    if len_lists > 10:
        modulo_label = len_lists // 10 + 1
        m_max_obs_labels = [f"{m_max_obs_list[idx]:.1f}" if idx % modulo_label == 0 else ""
                            for idx in range(len_lists)]
    else:
        m_max_obs_labels = [f"{m_max_obs_list[idx]:.1f}" for idx in range(len_lists)]
    axis.boxplot(lists, notch=notch, tick_labels=m_max_obs_labels,
                 flierprops=dict(marker='o', markerfacecolor='lightgray', markersize=1, markeredgecolor='none'))
    # for patch, color in zip(bplot['boxes'], colors):
    #     patch.set_color(color)
    # axis.tick_params("x", rotation=-25)
    if level is not None:
        axis.hlines(level, 0, len(lists) + 1, colors=None, linestyles='dotted', label=level_label)
        if level_label is not None:
            axis.legend()
    else:
        axis.plot(range(1, len_lists + 1), m_max_obs_list, color='gray', linestyle='dotted', label=r'$m_{max}$')


def delta_sel0(m_max_obs_dict, m_max_obs_list, key):
    lists = []
    for m_max_obs_val in m_max_obs_list:
        corrected_m_max_estimated = [max(val_m - val, -5)
                                     for val, val_m in zip(m_max_obs_dict[m_max_obs_val][key],
                                                           m_max_obs_dict[m_max_obs_val]['m_max'])]
        lists.append(corrected_m_max_estimated)
    return lists


def delta_sel1(m_max_obs_dict, m_max_obs_list, key):
    lists = []
    m_max_obs_list_solvable = []
    for m_max_obs_val in m_max_obs_list:
        corrected_m_max_estimated = [val_m - val
                                     for val, val_m, val_d in zip(m_max_obs_dict[m_max_obs_val][key],
                                                                  m_max_obs_dict[m_max_obs_val]['m_max'],
                                                                  m_max_obs_dict[m_max_obs_val]['m_max_direct'])
                                     if val_d is not None]
        if corrected_m_max_estimated:
            lists.append(corrected_m_max_estimated)
            m_max_obs_list_solvable.append(m_max_obs_val)
    return lists, m_max_obs_list_solvable


def delta_sel2(m_max_obs_dict, m_max_obs_list, beta):
    lists = []
    for m_max_obs_val in m_max_obs_list:
        corrected_m_max_estimated = [v_m - v_d if v_d is not None else v_m - 1 / beta - v_o
                                     for v_m, v_d, v_o in zip(m_max_obs_dict[m_max_obs_val]['m_max'],
                                                              m_max_obs_dict[m_max_obs_val]['m_max_direct'],
                                                              m_max_obs_dict[m_max_obs_val]['m_max_obs'])]
        lists.append(corrected_m_max_estimated)
    return lists


def delta_sel3(m_max_obs_dict, m_max_obs_list):
    lists = []
    for m_max_obs_val in m_max_obs_list:
        corrected_m_max_estimated = [val_m - val_d
                                     for val_m, val_d in zip(m_max_obs_dict[m_max_obs_val]['m_max'],
                                                             m_max_obs_dict[m_max_obs_val]['m_max_original'])]
        lists.append(corrected_m_max_estimated)
    return lists


def delta_sel4(m_max_obs_dict, m_max_obs_list):
    lists = []
    for m_max_obs_val in m_max_obs_list:
        corrected_m_max_estimated = [val_m - val_d
                                     for val_m, val_d in zip(m_max_obs_dict[m_max_obs_val]['m_max'],
                                                             m_max_obs_dict[m_max_obs_val]['m_max_obs'])]
        lists.append(corrected_m_max_estimated)
    return lists


def main(what=1):
    nr_catalogs = 25000
    m_max_range = (5.0, 8.5)
    m_min = 3.0
    beta = 2.3
    notch = False
    nr_mag_in_catalog = [v * p for p in (100, 1000, 10000) for v in (1, 2, 5)]
    fig, axes = plt.subplots(3, 3, sharex=False, sharey=True, gridspec_kw={'hspace': 0.35, "wspace": 0.02},
                             figsize=(12.0, 10.0))
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        axis = axes[axis_index // 3, axis_index % 3]
        m_max_obs_dict = rnd_m_max(nr_mag, beta, m_min, m_max_range, nr_catalogs)
        m_max_obs_list = sorted(list(m_max_obs_dict.keys()))
        print(f"{nr_mag}: {m_max_obs_list}")
        if what == 1:
            lists = [m_max_obs_dict[m_max_obs_val]['m_max'] for m_max_obs_val in m_max_obs_list]
            boxplot_m_max_obs(m_max_obs_list, lists,
                              f"{chr(97 + axis_index)}) $n(m_{{min}}={m_min})={nr_mag}$",
                              notch=notch, axis=axis)
            if axis_index % 3 == 0:
                axis.set_ylabel(r"$m_{max}$")
        if what == 2:
            lists = [m_max_obs_dict[m_max_obs_val]['m_max_obs'] for m_max_obs_val in m_max_obs_list]
            boxplot_m_max_obs(m_max_obs_list, lists,
                              f"{chr(97 + axis_index)}) $n(m_{{min}}={m_min})={nr_mag}$",
                              notch=notch, axis=axis)
            if axis_index % 3 == 0:
                axis.set_ylabel(r"$m_{max}^{obs}$")
        if what == 3:
            lists, m_max_obs_list_solvable = delta_sel1(m_max_obs_dict, m_max_obs_list, 'm_max_direct')
            boxplot_m_max_obs(m_max_obs_list_solvable, lists,
                              f"{chr(97 + axis_index)}) $n(m_{{min}}={m_min})={nr_mag}$",
                              notch=notch, axis=axis, level=0.0)
            if axis_index % 3 == 0:
                axis.set_ylabel(r"$m_{max}-\hat{m}_{max}$")
        if what == 4:
            lists = delta_sel2(m_max_obs_dict, m_max_obs_list, beta)
            boxplot_m_max_obs(m_max_obs_list, lists,
                              f"{chr(97 + axis_index)}) $n(m_{{min}}={m_min})={nr_mag}$",
                              notch=notch, axis=axis, level=0.0)
            if axis_index % 3 == 0:
                axis.set_ylabel(r"$m_{max}-\hat{m}_{max}$")
        if what == 5:
            lists = delta_sel0(m_max_obs_dict, m_max_obs_list, "m_max_original")

            boxplot_m_max_obs(m_max_obs_list, lists,
                              f"{chr(97 + axis_index)}) $n(m_{{min}}={m_min})={nr_mag}$",
                              notch=notch, axis=axis, level=0.0)
            if axis_index % 3 == 0:
                axis.set_ylabel(r"$m_{max}-\hat{m}_{max}$")
        if what == 6:
            lists, m_max_obs_list_solvable = delta_sel1(m_max_obs_dict, m_max_obs_list, 'm_max_original')
            boxplot_m_max_obs(m_max_obs_list_solvable, lists,
                              f"{chr(97 + axis_index)}) $n(m_{{min}}={m_min})={nr_mag}$",
                              notch=notch, axis=axis, level=0.0)
            if axis_index % 3 == 0:
                axis.set_ylabel(r"$m_{max}-\hat{m}_{max}$")
        if axis_index >= 6:
            axis.set_xlabel(r"$m_{max}^{obs}$")


if __name__ == "__main__":
    main(6)
    plt.show(block=True)
