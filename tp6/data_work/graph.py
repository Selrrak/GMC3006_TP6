import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import os
import pandas as pd
from data_work.actual_regression import do_regression
from data_work.reg_coef import r_coef
from data_work.parsers import parse_name
from data_work.parsers import parse_light_name
from data_work.parsers import parse_data_file
from data_work.parsers import parse_txt_file
from data_work.parsers import nbs_table_parser


def temp_results():
    mesures = [
        [23.9, 47.0],
        [20.3, 42.4],
        [25.9, 44.3],
        [23.5, 48.0],
    ]
    methode = [
        "thermomètre électronique",
        "TC avec sonde de réf. dans l'eau glacée",
        "TC avec module de compensation",
        "thermomètre à l'alcool",
    ]
    milieu = ["air ambient", "eau chaude"]
    df = pd.DataFrame(mesures, index=methode, columns=milieu)
    return df


def temp_data(path, action="get"):

    df = temp_results()
    filename = os.path.join(path, "temp_measures.pkl")
    if action == "save":
        df.to_pickle(filename)
        return None
    reg_pkl = pd.read_pickle(filename)
    return reg_pkl


def regression(t, a, b, c):
    reg = a * np.exp(-1 * t / b) + c
    return reg


def graph_exp(df):
    X = df["Temp. RTD"]
    K = 1000 * df["Type K"]
    J = 1000 * df["Type J"]
    E = 1000 * df["Type E"]
    fig, ax = plt.subplots()
    ax.plot(X, K, label="type K", marker="o")
    ax.plot(X, J, label="Type J", marker="x")
    ax.plot(X, E, label="type E", marker="^")
    ax.axhline(y=0, linestyle="--", linewidth=1, color="grey")
    ax.set_xlabel("Température (°C)")
    ax.set_ylabel("Tension (mV)")
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def graph_NBS(nbs_df, mesure):
    TC_type = mesure.columns.tolist()[1]
    T_mes = mesure["Temp. RTD"]
    V_mes = 1000 * mesure[TC_type]
    start = nbs_df.index[nbs_df["Temperature_C"] == -10][0]
    end = nbs_df.index[nbs_df["Temperature_C"] == 80][0]
    subset = nbs_df.loc[start:end]
    subset.to_csv("data.csv", index=False)
    T = subset["Temperature_C"]
    V = subset["Voltage_mV"]
    fig, ax = plt.subplots()
    ax.plot(T, V, label="valeur NBS", color="blue")
    if TC_type == "Type J":
        T_ref = 23
        V_ref_loc = nbs_df.index[nbs_df["Temperature_C"] == T_ref][0]
        V_ref = nbs_df["Voltage_mV"][V_ref_loc]
        ax.plot(T, V - V_ref, label="valeur NBS recalée", color="green")
    ax.plot(T_mes, V_mes, label="mesure", marker="o", color="orange")
    ax.axhline(y=0, linestyle="--", linewidth=1, color="grey")
    ax.set_xlabel("Température (°C)")
    ax.set_ylabel("Tension (mV)")
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def make_graphs_tp7(path):
    mesure = os.path.join(path, "data.txt")
    nbs_dir = os.path.join(path, "NBS_data")
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(mesure), ".."))
    save_dir = os.path.join(parent_dir, "graphs")

    plt.rcParams.update(
        {
            "text.usetex": True,  # render text with LaTeX
            "font.family": "serif",  # use serif font (Times)
            "font.serif": ["Times"],  # specify Times explicitly
            "font.size": 17,  # base font size for axes, labels, legends
            "axes.titlesize": 19,  # title size
            "axes.labelsize": 17,  # x/y labels
            "xtick.labelsize": 15,  # tick labels
            "ytick.labelsize": 15,
        }
    )
    df = parse_txt_file(mesure)
    exp = graph_exp(df)

    for filename in os.listdir(nbs_dir):
        name = filename[5]
        nbs_df = get_NBS_table(os.path.join(nbs_dir, filename))
        mesure = df[["Temp. RTD", f"Type {name}"]]
        nbs = graph_NBS(nbs_df, mesure)
        nbs.savefig(os.path.join(save_dir, f"{name}.png"), dpi=300, bbox_inches="tight")

    exp.savefig(os.path.join(save_dir, "mesures_TP7.png"), dpi=300, bbox_inches="tight")
    return None


def make_graph(path):
    plt.rcParams.update(
        {
            "text.usetex": True,  # render text with LaTeX
            "font.family": "serif",  # use serif font (Times)
            "font.serif": ["Times"],  # specify Times explicitly
            "font.size": 17,  # base font size for axes, labels, legends
            "axes.titlesize": 19,  # title size
            "axes.labelsize": 17,  # x/y labels
            "xtick.labelsize": 15,  # tick labels
            "ytick.labelsize": 15,
        }
    )
    df = parse_data_file(path)
    fig, ax = plt.subplots(figsize=(12, 6))
    filename = os.path.splitext(os.path.basename(path))[0]
    graphname = parse_name(filename)
    min = detect_min_deriv(df)
    dia, gamme = parse_light_name(filename)
    man_offset = 500
    if dia == "0.005 in" and gamme == "[-50;50] mV":
        man_offset = 50
    elif dia == "0.005 in" and gamme != "[-50;50] mV":
        man_offset = 10000
    if dia == "0.01 in":
        man_offset = 300
    if dia == "0.02 in":
        man_offset = 190
    if dia == "0.032 in":
        man_offset = 455
    start = int(min[0] * 10000) - man_offset
    a, b, c = do_regression(path, start)
    time_series = (df["X_Value"][start:] - df["X_Value"][start]).to_numpy()
    voltage = (df["Tension"][start:] * 1000).to_numpy()

    reg = regression(time_series, a, b, c)
    ax.scatter(time_series, voltage, label="mesurée", s=2)
    ax.grid(True)
    ax.plot(time_series, reg * 1000, label="modèle", color="orange")
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Tension (mV)")
    ax.legend(loc="center right")
    c_symbol = "+"
    if c < 0:
        c_symbol = "-"
    a, b, c = round(1000 * a, 6), round(b, 6), round(abs(1000 * c), 6)

    parent_dir = os.path.abspath(os.path.join(path, "..", ".."))
    main_dir = os.path.join(parent_dir, "tp6")
    r_coef(main_dir, "edit", TC=f"{filename}.lvm", new_coefs=[a, b, c])

    ax.text(
        x=0.45,
        y=0.85,  # coordinates in axes fraction
        s=f"V = {a}*exp(-t/{b}){c_symbol}{c}",
        transform=ax.transAxes,  # important: use axes coordinates
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=17,
        color="black",
    )

    parent_dir = os.path.abspath(os.path.join(os.path.dirname(path), ".."))
    plot_dir = os.path.join(parent_dir, "Rapport_TP6_7_GMC3006", "graphs")
    save_path = os.path.join(plot_dir, f"{filename}no_title.png")
    save_path_w_title = os.path.join(plot_dir, f"{filename}.png")
    os.makedirs(plot_dir, exist_ok=True)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    ax.set_title(graphname)
    fig.savefig(save_path_w_title, dpi=300, bbox_inches="tight")
    return None


def detect_min_deriv(df):
    derivative = np.gradient(df["Tension"], df["X_Value"])
    window = 100
    weights = np.ones(window) / window
    smoothed = np.convolve(derivative, weights, mode="same")

    min_idx = np.argmin(smoothed)
    x_at_min = df["X_Value"].iloc[min_idx]
    y_at_min = df["Tension"].iloc[min_idx]
    return x_at_min, y_at_min


def make_tables(rc_df, path):
    parent_dir = os.path.dirname(path)
    table_dir = os.path.join(parent_dir, "Rapport_TP6_7_GMC3006", "graphs")
    os.makedirs(table_dir, exist_ok=True)

    save_path_tau = os.path.join(table_dir, "tau_table.png")
    save_path_temp = os.path.join(table_dir, "temp_table.png")

    col = rc_df["b"]
    filenames = [name[:-4] for name in col.index]

    TCs = [f"{parse_light_name(name)[0]}" for name in filenames]
    gammes = [f"{parse_light_name(name)[1]}" for name in filenames]
    cell_data = [[gamme, tau] for gamme, tau in zip(gammes, col)]

    fig, ax = plt.subplots()
    ax.axis("off")

    table = ax.table(
        cellText=cell_data,
        rowLabels=TCs,
        colLabels=["gamme de prise de mesure", "constante de temps [s]"],
        loc="center",
    )
    for cell in table.get_celld().values():
        cell.set_text_props(ha="center", va="center")
    fig.savefig(save_path_tau, dpi=300, bbox_inches="tight")

    temp_data(os.getcwd(), "save")
    t_df = temp_data(os.getcwd(), "get")

    fig, ax = plt.subplots()
    ax.axis("off")

    if isinstance(t_df, pd.DataFrame):
        table = ax.table(
            cellText=t_df.values.tolist(),
            rowLabels=list(t_df.index),
            colLabels=list(t_df.columns),
            loc="center",
        )

        fig.canvas.draw()  # needed to compute positions

        # cells we want the header to span
        left_cell = table[(0, 0)]
        right_cell = table[(0, len(t_df.columns) - 1)]

        # bounding boxes in display coords
        renderer = fig.canvas.get_renderer()
        bbox_left = left_cell.get_window_extent(renderer)
        bbox_right = right_cell.get_window_extent(renderer)

        # convert to axis coordinates
        inv = ax.transAxes.inverted()
        x0, y0 = inv.transform((bbox_left.x0, bbox_left.y1))
        x1, y1 = inv.transform((bbox_right.x1, bbox_right.y1))

        width = x1 - x0
        height = inv.transform((0, bbox_left.y1 + bbox_left.height))[1] - y0

        # draw rectangle
        rect = Rectangle((x0, y0), width, height, transform=ax.transAxes, fill=False)
        ax.add_patch(rect)

        # centered label
        ax.text(
            x0 + width / 2,
            y0 + height / 2,
            "Température en fonction du milieu [°C]",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        for cell in table.get_celld().values():
            cell.set_text_props(ha="center", va="center")

        fig.savefig(save_path_temp, dpi=300, bbox_inches="tight")
    return None


def get_NBS_table(path):
    df = nbs_table_parser(path)
    return df
