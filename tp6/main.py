import data_work.graph as graph
import os
import pandas as pd

reg_coef = [
    [0.1, 0.1, 0.01],
    [0.1, 0.1, 0.01],
    [0.1, 0.1, 0.01],
    [0.1, 0.1, 0.01],
    [0.1, 0.1, 0.01],
    [0.1, 0.1, 0.01],
    [0.1, 0.1, 0.01],
    [0.1, 0.1, 0.01],
]
datafiles = [
    "TC_0005_s_filtre_10v_1.lvm",
    "TC_0005_s_filtre_10v_2.lvm",
    "TC_0005_filtre_10v.lvm",
    "TC_0005_s_filtre_50mv.lvm",
    "TC_010_s_filtre.lvm",
    "TC_0020_s_filtre.lvm",
    "TC_0032_s_filtre.lvm",
    "TC_0032_filtre.lvm",
]
coef_letters = ["a", "b", "c"]
df = pd.DataFrame(reg_coef, index=datafiles, columns=coef_letters)


def main():
    cwd = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(cwd, ".."))
    data_dir = os.path.join(parent_dir, "TP6_data")

    for filename in os.listdir(data_dir):
        if not filename.lower().endswith(".lvm"):
            continue

        file_path = os.path.join(data_dir, filename)

        if os.path.isfile(file_path):
            print(f"processing {filename}")
            print(
                f"a={df.loc[filename,"a"]},b={df.loc[filename,"b"]},c={df.loc[filename,"c"]}"
            )
            graph.make_graph(file_path)


if __name__ == "__main__":
    main()
