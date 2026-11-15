import numpy as np
import sicate.gr as gr
import matplotlib.pyplot as plt


def simulate_m_max_obs_prob(nr_catalogs, nr_mag_in_catalog, m_max_list, m_max_obs_list, beta, m_min,
                            axes, axes_columns, step):
    colors = plt.cm.tab10
    markers = ['o', 'v', '^', 's', 'd', '>', '<', '+', 'x', '*']
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        axis = axes[axis_index // axes_columns, axis_index % axes_columns]
        print(f"n={nr_mag}")
        for m_max_idx, m_max in enumerate(m_max_list):
            print(f"{nr_mag}: m_max={m_max}")
            m_max_obs_dict = {f"{m_max_obs:.1f}": 0 for m_max_obs in m_max_obs_list}
            for _ in range(nr_catalogs):
                mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
                m_max_obs = np.max(mag_v)
                if m_max_obs < m_max_obs_list[0]:
                    m_max_obs = m_max_obs_list[0]
                m_max_obs_d = np.round(m_max_obs / step) * step
                m_max_obs_dict[f"{m_max_obs_d:.1f}"] += 1
            y = [m_max_obs_dict[f"{m_max_obs:.1f}"] / nr_catalogs for m_max_obs in m_max_obs_list]
            axis.plot(m_max_obs_list, y, color=colors.colors[m_max_idx], label=f"$m_{{max}}={m_max:.1f}$",
                      marker=markers[m_max_idx], markersize=4)
            # axis.plot(m_max_obs_list, y, color=colors.colors[m_max_idx], label=f"$m_{{max}}={m_max:.1f}$")
        if len(nr_mag_in_catalog) - axis_index <= axes_columns:
            axis.set_xlabel(r"$m_{max}^{obs}$", size=12)
        if axis_index % axes_columns == 0:
            axis.set_ylabel(rf"probability in $\pm${step / 2} range", size=12)
        if not axis_index:
            axis.legend()
        axis.set_title(f"{chr(97 + axis_index)}) $n(m_{{c}}={m_min})={nr_mag}$", loc='left')


def compute_m_max_obs_pdf(nr_mag_in_catalog, m_max_list, m_max_obs_list, beta, m_min,
                          axes, axes_columns):
    colors = plt.cm.tab10
    markers = ['o', 'v', '^', 's', 'd', '>', '<', '+', 'x', '*']
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        axis = axes[axis_index // axes_columns, axis_index % axes_columns]
        for m_max_idx, m_max in enumerate(m_max_list):
            pdf_list = [(nr_mag * gr.cdf(m_max_obs, beta, m_min, m_max) ** (nr_mag - 1)
                         * gr.pdf(m_max_obs, beta, m_min, m_max))[0]
                        for m_max_obs in m_max_obs_list]
            # axis.plot(m_max_obs_list, pdf_list, color=colors.colors[m_max_idx],
            #           label=f"$m_{{max}}={m_max:.1f}$", marker=markers[m_max_idx], markersize=4)
            axis.plot(m_max_obs_list, pdf_list, color=colors.colors[m_max_idx], label=f"$m_{{max}}={m_max:.1f}$")
        if len(nr_mag_in_catalog) - axis_index <= axes_columns:
            axis.set_xlabel(r"$m_{max}^{obs}$", size=12)
        if axis_index % axes_columns == 0:
            axis.set_ylabel(r"pdf of $m_{max}^{obs}$", size=12)
        if not axis_index:
            axis.legend()
        axis.set_title(f"{chr(97 + axis_index)}) $n(m_{{c}}={m_min})={nr_mag}$", loc='left')


def compute_m_max_obs_cdf(nr_mag_in_catalog, m_max_list, m_max_obs_list, beta, m_min,
                          axes, axes_columns):
    colors = plt.cm.tab10
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        axis = axes[axis_index // axes_columns, axis_index % axes_columns]
        for m_max_idx, m_max in enumerate(m_max_list):
            cdf_list = [gr.cdf(m_max_obs, beta, m_min, m_max) ** nr_mag for m_max_obs in m_max_obs_list]
            axis.plot(m_max_obs_list, cdf_list, color=colors.colors[m_max_idx], label=f"$m_{{max}}={m_max:.1f}$")
        if len(nr_mag_in_catalog) - axis_index <= axes_columns:
            axis.set_xlabel(r"$m_{max}^{obs}$", size=12)
        if axis_index % axes_columns == 0:
            axis.set_ylabel(r"CDF of $m_{max}^{obs}$", size=12)
        if not axis_index:
            axis.legend()
        axis.set_title(f"{chr(97 + axis_index)}) $n(m_{{c}}={m_min})={nr_mag}$", loc='left')


def compute_m_max_obs_prob(nr_mag_in_catalog, m_max_list, m_max_obs_list, beta, m_min,
                           axes, axes_columns, step):
    colors = plt.cm.tab10
    markers = ['o', 'v', '^', 's', 'd', '>', '<', '+', 'x', '*']
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        axis = axes[axis_index // axes_columns, axis_index % axes_columns]
        for m_max_idx, m_max in enumerate(m_max_list):
            m_max_obs_range = step / 2
            p_max_obs_list = []
            p_not_max_obs_list = []
            prob_list = []
            for m_max_obs in m_max_obs_list:
                m_max_range = (m_max_obs - m_max_obs_range, m_max_obs + m_max_obs_range)
                cdf_h = np.exp(-nr_mag * (1 - gr.cdf(m_max_obs + m_max_obs_range, beta, m_min, m_max)))
                cdf_l = np.exp(-nr_mag * (1 - gr.cdf(m_max_obs - m_max_obs_range, beta, m_min, m_max)))
                p_max_obs = cdf_h - cdf_l
                p_not_max_obs = cdf_h
                prob = p_max_obs * p_not_max_obs
                p_max_obs_list.append(p_max_obs)
                p_not_max_obs_list.append(p_not_max_obs)
                prob_list.append(prob)
            axis.plot(m_max_obs_list, prob_list, color=colors.colors[m_max_idx], label=f"$m_{{max}}={m_max:.1f}$",
                      marker=markers[m_max_idx], markersize=4)
            # axis.plot(m_max_obs_list, p_not_max_obs_list, color=colors.colors[m_max_idx],
            #           label=f"$m{{max}}={m_max:.1f}$", marker=markers[m_max_idx], markersize=6, linestyle='dotted')
            # axis.plot(m_max_obs_list, p_max_obs_list, color=colors.colors[m_max_idx], label=f"$m{{max}}={m_max:.1f}$",
            #           marker=markers[m_max_idx], markersize=6, linestyle='dashed')
        if len(nr_mag_in_catalog) - axis_index <= axes_columns:
            axis.set_xlabel(r"$m_{max}^{obs}$", size=12)
        if axis_index % axes_columns == 0:
            axis.set_ylabel(rf"probability in $\pm${m_max_obs_range} range", size=12)
        if not axis_index:
            axis.legend()
        axis.set_title(f"{chr(97 + axis_index)}) $n(m_{{c}}={m_min})={nr_mag}$", loc='left')


def plot_results():
    nr_catalogs = 10000
    m_max_range = (6.0, 8.5)
    m_min = 3.0
    nr_mag_min = 100
    beta = 2.3
    notch = False
    max_num = 6
    step = 0.5

    nr_mag_in_catalog = [v * p for p in (nr_mag_min, 10 * nr_mag_min, 100 * nr_mag_min) for v in (1, 2, 5)]
    fig, axes = plt.subplots(3, 3, sharex=True, sharey=False, gridspec_kw={'hspace': 0.15, "wspace": 0.12},
                             figsize=(12.0, 10.0))
    m_max_list = np.linspace(m_max_range[0], m_max_range[1], num=max_num)
    # m_max_obs_list = np.arange(4.5, 9.0, step)
    # compute_m_max_obs_prob(nr_mag_in_catalog, m_max_list, m_max_obs_list, beta, m_min, axes, 3, step)
    m_max_obs_list = np.arange(4.5, 9.0, 0.001)
    # compute_m_max_obs_pdf(nr_mag_in_catalog, m_max_list, m_max_obs_list, beta, m_min, axes, 3)
    compute_m_max_obs_cdf(nr_mag_in_catalog, m_max_list, m_max_obs_list, beta, m_min, axes, 3)
    # simulate_m_max_obs_prob(nr_catalogs, nr_mag_in_catalog, m_max_list, m_max_obs_list, beta, m_min, axes, 3, step)
    plt.show(block=True)


if __name__ == "__main__":
    plot_results()