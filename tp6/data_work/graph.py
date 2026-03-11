import lvm.lvm as lvm
import matplotlib.pyplot as plt
import numpy as np
import os


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
    elif (parts[2] != "mod") & (parts[2] != "sonde"):
        filtre = " acquisition filtrée"
    else:
        filtre = "filtre non applicable"

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
        f"tension mesurée et modélisée d'un thermocouple {TC_size}"
        + "\n"
        + f"{filtre}, gamme = {gamme}, {it}"
    )
    return name


def regression(a, b, c):
    t = np.arange(0, 3 + 0.0001, 0.0001)
    reg = a * np.exp(-1 * t / b) + c
    return reg


def make_graph(path):
    raw_df = lvm.parse_lvm(path)
    df = raw_df.drop(columns=["Comment"], errors="ignore")
    fig, ax = plt.subplots()
    filename = os.path.splitext(os.path.basename(path))[0]
    graphname = parse_name(filename)

    ax.plot(df["X_Value"], df["Tension"], label="mesurée")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title(graphname)
    ax.legend()

    parent_dir = os.path.abspath(os.path.join(os.path.dirname(path), ".."))
    plot_dir = os.path.join(parent_dir, "graphs")
    save_path = os.path.join(plot_dir, f"{filename}.png")
    os.makedirs(plot_dir, exist_ok=True)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()

    return 0
