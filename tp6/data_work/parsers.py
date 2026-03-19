import lvm.lvm as lvm
import pandas as pd
import io


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


def parse_data_file(path):
    raw_df = lvm.parse_lvm(path)
    df = raw_df.drop(columns=["Comment"], errors="ignore")
    return df


def parse_txt_file(path: str) -> pd.Dataframe:
    df = pd.read_csv(path, sep="\t", dtype=float)
    return df


def nbs_table_parser(path):
    """
    Parse an NBS-style thermocouple table.

    Assumes:
    - First column: base temperature (0, 10, 20, …)
    - Columns 1-11: incremental digits (0-10)
    - Values: voltage in mV
    Returns a DataFrame with columns: Temperature_C, Voltage_mV
    """
    data = []
    with open(path, "rt", encoding="latin1") as f:
        for line in f:
            line = line.strip()
            if line.startswith("***"):
                break
            # skip empty lines, header lines, or lines containing "thermo" or "mV"
            if not line or "thermo" in line.lower() or "mV" in line:
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            # skip lines where the first column is not a number
            try:
                base_temp = float(parts[0])
            except ValueError:
                continue
            voltages = parts[1:]

            for i, v in enumerate(voltages):
                if float(v) != 0.0:
                    sign = float(v) / abs(float(v))
                else:
                    sign = 1
                temp = base_temp + sign * i
                data.append({"Temperature_C": temp, "Voltage_mV": float(v)})

    df = pd.DataFrame(data)
    return df
