import os
import pandas as pd


def generate_df():
    reg_coef = [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
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


def r_coef(path, action, TC=None, new_coefs=None):
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, "reg_coef.pkl")

    if action == "gen":
        df = generate_df()
        df.to_pickle(filename)
        return None

    if action == "get":
        reg_pkl = pd.read_pickle(filename)
        return reg_pkl

    if action == "edit" and TC is not None and new_coefs is not None:
        reg = r_coef(path, "get")
        reg.loc[TC] = new_coefs
        reg.to_pickle(filename)
        return None
