import numpy as np
import sicate.gr as gr
import sicate.ks as ks
from sicate.test_utils import plot_one_boxplot, plot_points_n
import matplotlib.pyplot as plt


def test_ks(nr_mags, beta, m_min, m_max, nr_catalogs):
    ks_list = []
    ks_iter_list = []
    m_max_obs_list = []
    for nr_mag in nr_mags:
        ks_v = []
        ks_iter_v = []
        m_max_obs_v = []
        for _ in range(nr_catalogs):  # LOOP OF CATALOGUES ===========
            mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
            m_max_obs = np.max(mag_v)
            ks_v.append(ks.m_max_simple(m_max_obs, nr_mag, beta, m_min))
            ks_iter_v.append(ks.m_max_solve(m_max_obs, nr_mag, beta, m_min))
            m_max_obs_v.append(m_max_obs)
        ks_list.append(ks_v)
        ks_iter_list.append(ks_iter_v)
        m_max_obs_list.append(m_max_obs_v)
    return ks_list, ks_iter_list, m_max_obs_list


def test_m_max_estimate(nr_mag, beta, m_min, m_max, nr_catalogs):
    m_max_obs_list = []
    m_max_original_list = []
    m_max_direct_list = []
    for _ in range(nr_catalogs):  # LOOP OF CATALOGUES ===========
        mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
        m_max_obs = np.max(mag_v)
        mag_o = ks.m_max_simple(m_max_obs, nr_mag, beta, m_min)
        mag_d = ks.m_max_solve(m_max_obs, nr_mag, beta, m_min)
        m_max_obs_list.append(m_max_obs)
        m_max_original_list.append(mag_o)
        m_max_direct_list.append(mag_d)
    return m_max_obs_list, m_max_original_list, m_max_direct_list


def simulate_solution_existence1():
    nr_catalogs = 1000
    # nr_catalogs = 100
    m_max_range = (6.0, 8.5)
    m_min = 3.0
    beta = 2.3
    nr_mag_in_catalog = [v * p for p in (10, 100, 1000, 10000) for v in (10, 12, 16, 20, 25, 32, 40, 50, 63, 80)]
    # nr_mag_in_catalog = [v * p for p in (10, 100, 1000) for v in (10, 20, 50)]
    print(f"nr_mag_in_catalog={nr_mag_in_catalog}")
    fig1, axis1 = plt.subplots()
    for idx, m_max in enumerate(np.linspace(m_max_range[0], m_max_range[1], num=6)):
        print(f"{idx}: m_max={m_max}")
        ks_orig_list, ks_iter_list, m_max_obs_list = test_ks(nr_mag_in_catalog, beta, m_min, m_max, nr_catalogs)
        solvable_ks_iter_list = [[ks_i for ks_i in ks_iter_v if ks_i is not None] for ks_iter_v in ks_iter_list]
        solutions = [len(ks_i) / nr_catalogs for ks_i in solvable_ks_iter_list]
        plot_points_n(nr_mag_in_catalog, solutions, axis=axis1, idx=idx, m_max=m_max)
    axis1.hlines(0.95, nr_mag_in_catalog[0], nr_mag_in_catalog[-1], linestyles='dotted', label=r'$\alpha = 0.05$')
    axis1.set_title("K-S estimator solution ratio")
    axis1.set_xlim(nr_mag_in_catalog[0] / 1.1, nr_mag_in_catalog[-1] * 1.1)
    axis1.set_xlabel(f"$n(m_{{c}}={m_min})$")
    axis1.legend()


def simulate_solution_existence():
    nr_catalogs = 10000
    m_max_range = (6.0, 8.5)
    m_min = 3.0
    beta = 2.3
    nr_mag_in_catalog = [v * p for p in (1, 10, 100, 1000) for v in (10, 12, 16, 20, 25, 32, 40, 50, 63, 80)]
    print(f"nr_mag_in_catalog={nr_mag_in_catalog}")
    fig1, axis1 = plt.subplots()
    for idx, m_max in enumerate(np.linspace(m_max_range[0], m_max_range[1], num=6)):
        print(f"{idx}: m_max={m_max}")
        solutions_list = []
        for nr_mag in nr_mag_in_catalog:
            nr_solutions = 0
            for _ in range(nr_catalogs):
                mag_v = gr.rnd_mag(nr_mag, beta, m_min, m_max)
                m_max_obs = np.max(mag_v)
                if ks.condition(m_max_obs, nr_mag, beta, m_min):
                    nr_solutions += 1
            solutions_list.append(nr_solutions / nr_catalogs)
        plot_points_n(nr_mag_in_catalog, solutions_list, axis=axis1, idx=idx, m_max=m_max)
    axis1.hlines(0.95, nr_mag_in_catalog[0], nr_mag_in_catalog[-1], linestyles='dotted', label=r'$\alpha = 0.05$')
    axis1.set_title("K-S estimator solution ratio")
    axis1.set_xlim(nr_mag_in_catalog[0] / 1.1, nr_mag_in_catalog[-1] * 1.1)
    axis1.set_xlabel(f"$n(m_{{c}}={m_min})$")
    axis1.legend()


def simulate_m_max_estimate(m_min=3.0, beta=2.3):
    nr_catalogs = 1000
    m_max_range = (6.0, 8.5)
    notch = False
    max_num = 10
    nr_mag_in_catalog = [v * p for p in (100, 1000, 10000) for v in (1, 2, 5)]
    fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, gridspec_kw={'hspace': 0.15, "wspace": 0.02},
                             figsize=(12.0, 10.0))
    m_max_list = np.linspace(m_max_range[0], m_max_range[1], num=max_num)
    for axis_index, nr_mag in enumerate(nr_mag_in_catalog):
        print(f"n={nr_mag}")
        m_max_solved_lists = []
        m_max_simple_lists = []
        m_max_simple1_lists = []
        for idx, m_max in enumerate(m_max_list):
            print(f"{nr_mag}: m_max={m_max}")
            obs_list, simple_list, solved_list = test_m_max_estimate(nr_mag, beta, m_min, m_max, nr_catalogs)
            m_max_solved_lists.append([v_d for v_d in solved_list if v_d is not None])
            m_max_simple_lists.append(simple_list)
            m_max_simple1_lists.append([v_o for v_o, v_d in zip(simple_list, solved_list) if v_d is not None])
        plot_one_boxplot(axes, axis_index, m_max_solved_lists, m_max_list, m_min, nr_mag, notch=notch)
        plot_one_boxplot(axes, axis_index, m_max_simple_lists, m_max_list, m_min, nr_mag, notch=notch)
        plot_one_boxplot(axes, axis_index, m_max_simple1_lists, m_max_list, m_min, nr_mag, notch=notch)


if __name__ == "__main__":
    simulate_solution_existence()
    # simulate_m_max_estimate()
    plt.show(block=True)
