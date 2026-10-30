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
        m_max_obs = round(np.max(mag_v) * 5) / 5
        # m_max_obs = np.round(np.max(mag_v), decimals=1)
        if m_max_obs not in m_max_obs_dict:
            m_max_obs_dict[m_max_obs] = {'m_max': [], 'm_max_direct': [], 'm_max_original': []}
        m_max_obs_dict[m_max_obs]['m_max_original'].append(m_max_original(m_max_obs, nr_mag, beta, m_min))
        m_max_obs_dict[m_max_obs]['m_max_direct'].append(m_max_direct(m_max_obs, nr_mag, beta, m_min))
        m_max_obs_dict[m_max_obs]['m_max'].append(m_max)
    return m_max_obs_dict


def boxplot_m_max_obs(m_max_obs_list, lists, title, corected=1000, level=None, level_label=None,
                      notch=False, axis=None):
    if axis is None:
        figure, axis = plt.subplots()
    axis.set_title(title)
    colors = ['k' if idx < corected else 'm' for idx in range(len(lists))]
    bplot = axis.boxplot(lists, notch=notch, sym='k.', tick_labels=m_max_obs_list[:len(lists)])
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_color(color)
    # axis.tick_params("x", rotation=45)
    if level is not None:
        axis.hlines(level, 0, len(lists) + 1, colors=None, linestyles='dotted', label=level_label)
        if level_label is not None:
            axis.legend()


def corrected(m_max_obs_dict, m_max_obs_list, key):
    lists = []
    for m_max_obs_val in m_max_obs_list:
        corrected_m_max_estimated = [val for val, val_direct in zip(m_max_obs_dict[m_max_obs_val][key],
                                                                    m_max_obs_dict[m_max_obs_val]['m_max_direct'])
                                     if val_direct is not None]
        lists.append(corrected_m_max_estimated)
    return lists


def delta_sel(m_max_obs_dict, m_max_obs_list, key):
    lists = []
    for m_max_obs_val in m_max_obs_list:
        corrected_m_max_estimated = [val_m - val
                                     for val, val_m, val_d in zip(m_max_obs_dict[m_max_obs_val][key],
                                                                  m_max_obs_dict[m_max_obs_val]['m_max'],
                                                                  m_max_obs_dict[m_max_obs_val]['m_max_direct'])
                                     if val_d is not None]
        if corrected_m_max_estimated:
            lists.append(corrected_m_max_estimated)
    return lists


def delta_sel2(m_max_obs_dict, m_max_obs_list, beta):
    lists = []
    for m_max_obs_val in m_max_obs_list:
        corrected_m_max_estimated = [val_m - val_d if val_d is not None else val_m - 1 / beta - m_max_obs_val
                                     for val_m, val_d in zip(m_max_obs_dict[m_max_obs_val]['m_max'],
                                                             m_max_obs_dict[m_max_obs_val]['m_max_direct'])]
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

def main():
    nr_catalogs = 20000
    m_max_range = (6.5, 7.5)
    m_min = 3.0
    beta = 2.3
    notch = False
    # m_max_text = r"$m_{max}$"
    # m_max_diff_text = r"$m_{max}-\hat{m}_{max}$"
    # delta_text = r"$\Delta$"
    nr_mag_in_catalog = [v * p for p in (100, 1000, 10000) for v in (1, 2, 5)]
    fig, axes = plt.subplots(3, 3)
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        m_max_obs_dict = rnd_m_max(nr_mag, beta, m_min, m_max_range, nr_catalogs)
        m_max_obs_list = sorted(list(m_max_obs_dict.keys()))
        print(f"{nr_mag}: {m_max_obs_list}")
        # # lists = [m_max_obs_dict[m_max_obs_val]['m_max'] for m_max_obs_val in m_max_obs_list]
        # # boxplot_m_max_obs(m_max_obs_list, lists, f"{nr_mag} magnitudes: real {m_max_text}", notch=notch)
        # # lists = [m_max_obs_dict[m_max_obs_val]['m_max_original'] for m_max_obs_val in m_max_obs_list]
        lists1 = delta_sel(m_max_obs_dict, m_max_obs_list, 'm_max_direct')
        lists = delta_sel3(m_max_obs_dict, m_max_obs_list)
        axis = axes[axis_index % 3, axis_index // 3]
        # boxplot_m_max_obs(m_max_obs_list[:8], lists[:8], f"{nr_mag} events", corected=len(lists1),
        #                   notch=notch, axis=axis, level=0)
        boxplot_m_max_obs(m_max_obs_list[:8], lists[:8], f"{nr_mag} events",
                          notch=notch, axis=axis, level=0)
        if axis_index % 3 == 2:
            axis.set_xlabel(r"$m_{max}^{obs}$")
        if axis_index < 3:
            axis.set_ylabel(r"$m_{max}-\hat{m}_{max}$")

    plt.show(block=True)


if __name__ == "__main__":
    main()