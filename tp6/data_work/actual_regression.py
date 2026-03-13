import numpy as np
from scipy.optimize import curve_fit
from data_work.parsers import parse_data_file


def do_regression(path, start):
    df = parse_data_file(path)
    window = 1
    weights = np.ones(window) / window
    df["Tension_smooth"] = np.convolve(df["Tension"], weights, mode="same")

    df = df[start:]
    df["X_Value"] = df["X_Value"] - df["X_Value"][start]
    x = df["X_Value"].to_numpy()
    y = df["Tension_smooth"].to_numpy()
    print("doing regression")

    def model(t, a, b, c):
        return (a) * np.exp(-(t / b)) + c

    params, pcov = curve_fit(
        model,
        x,
        y,
        p0=[0.1, 0.1, 0.001],
        maxfev=7000,
    )
    print(np.sqrt(np.diag(pcov)))
    return params
