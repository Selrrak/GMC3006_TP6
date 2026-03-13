import numpy as np
from scipy.optimize import curve_fit
from data_work.parsers import parse_data_file


def model(t, a, b, c):
    return a * np.exp(-1 * t / b) + c


def do_regression(path, start):
    df = parse_data_file(path)
    df = df[start:]
    print("doing regression")
    x, y = df["X_Value"], df["Tension"]
    params, _ = curve_fit(model, x, y, maxfev=3000)
    return params
