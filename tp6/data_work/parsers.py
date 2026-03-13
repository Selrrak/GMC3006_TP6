import lvm.lvm as lvm


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
