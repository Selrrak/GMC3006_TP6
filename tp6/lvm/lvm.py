import pandas as pd
import io


def parse_lvm(path: str) -> pd.DataFrame:

    header_count = 0
    buf = io.StringIO()

    with open(path, "rt") as lvm:
        for line in lvm:
            if line.strip().startswith("***End_of_Header***"):
                header_count += 1
                continue
            if header_count >= 2:
                buf.write(line)

    buf.seek(0)
    return pd.read_csv(buf, sep="\t", decimal=",")
