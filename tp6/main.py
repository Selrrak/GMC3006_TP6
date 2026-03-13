import data_work.graph as graph
import data_work.reg_coef as rc
import os


def main():
    cwd = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(cwd, ".."))
    data_dir = os.path.join(parent_dir, "TP6_data")
    rc.r_coef(cwd, action="save")
    rc_df = rc.r_coef(cwd, action="get")
    graph.make_tables(rc_df, cwd)
    for filename in os.listdir(data_dir):
        if not filename.lower().endswith(".lvm"):
            continue

        file_path = os.path.join(data_dir, filename)

        if os.path.isfile(file_path):
            print(f"processing {filename}")
            graph.make_graph(file_path)


if __name__ == "__main__":
    main()
