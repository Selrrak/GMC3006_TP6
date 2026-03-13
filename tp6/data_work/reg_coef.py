import os
import pandas as pd


def rc_results():
    reg_coef = [
        [0.1, 0.1, 0.01],
        [0.1, 0.1, 0.01],
        [0.1, 0.1, 0.01],
        [0.1, 0.1, 0.01],
        [0.1, 0.1, 0.01],
    ]
    datafiles = [
        "TC_0005_s_filtre_10v_2.lvm",
        "TC_0005_s_filtre_50mv.lvm",
        "TC_010_s_filtre.lvm",
        "TC_0020_s_filtre.lvm",
        "TC_0032_s_filtre.lvm",
    ]
    coef_letters = ["a", "b", "c"]
    df = pd.DataFrame(reg_coef, index=datafiles, columns=coef_letters)
    return df


def r_coef(path, action="get"):

    df = rc_results()
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, "reg_coef.pkl")
    if action == "save":
        df.to_pickle(filename)
        return None
    reg_pkl = pd.read_pickle(filename)
    return reg_pkl
