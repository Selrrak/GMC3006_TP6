import lvm.lvm as lvm
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from data_work.reg_coef import r_coef


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


def parse_name(filename):
    parts = filename.split("_")
    TC_size = parts[1]
    try:
        TC_size = float(TC_size) / 1000.0
        TC_size = f"D = {TC_size} in"
    except:
        TC_size = "artisanal"
    if parts[2] == "s":
        filtre = "acquisition non filtrée"
    else:
        filtre = " acquisition filtrée"

    if any("v" in part.lower() for part in parts):
        if any("m" in part.lower() for part in parts):
            gamme = "[-50;50] mV"
        else:
            gamme = "[-10;10] V"
    else:
        gamme = "[-50;50] mV"

    try:
        it = int(parts[-1])
        it = f"essai {it}"
    except:
        it = "essai 1"

    name = (
        f"tension mesurée et modélisée d'un thermocouple {TC_size} plongé dans de l'eau glacée"
        + "\n"
        + f"{filtre}, gamme = {gamme}, {it}"
    )
    return name


def parse_light_name(filename):
    parts = filename.split("_")
    TC_size = parts[1]
    if any("v" in part.lower() for part in parts):
        if any("m" in part.lower() for part in parts):
            gamme = "[-50;50] mV"
        else:
            gamme = "[-10;10] V"
    else:
        gamme = "[-50;50] mV"

    return f"{float(TC_size)/1000} in", gamme


def regression(a, b, c):
    t = np.arange(0, 3, 0.0001)
    reg = a * np.exp(-1 * t / b) + c
    return reg


def make_graph(path):
    raw_df = lvm.parse_lvm(path)
    df = raw_df.drop(columns=["Comment"], errors="ignore")
    fig, ax = plt.subplots()
    filename = os.path.splitext(os.path.basename(path))[0]
    main_dir = os.path.abspath(os.path.join(os.getcwd()))
    graphname = parse_name(filename)
    rc_df = r_coef(main_dir, "get")
    if rc_df is not None:
        a, b, c = (
            rc_df.loc[f"{filename}.lvm", "a"],
            rc_df.loc[f"{filename}.lvm", "b"],
            rc_df.loc[f"{filename}.lvm", "c"],
        )
    else:
        a, b, c = (0, 0, 0)
    reg = regression(a, b, c)

    ax.plot(df["X_Value"], df["Tension"], label="mesurée")
    ax.plot(df["X_Value"], reg, label="modèle")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title(graphname)
    ax.legend()

    parent_dir = os.path.abspath(os.path.join(os.path.dirname(path), ".."))
    plot_dir = os.path.join(parent_dir, "graphs")
    save_path = os.path.join(plot_dir, f"{filename}.png")
    os.makedirs(plot_dir, exist_ok=True)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return None


def make_tables(rc_df, path):
    parent_dir = os.path.dirname(path)
    table_dir = os.path.join(parent_dir, "graphs")
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
        colLabels=["gamme de prise de mesure", "constante de temps"],
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
    for cell in table.get_celld().values():
        cell.set_text_props(ha="center", va="center")

    fig.savefig(save_path_temp, dpi=300, bbox_inches="tight")
    return None
