import numpy as np
from scipy.optimize import curve_fit
from data_work.parsers import parse_data_file


def do_regression(path, start):
    df = parse_data_file(path)
    window = 500
    weights = np.ones(window) / window
    df["Tension_smooth"] = np.convolve(df["Tension"], weights, mode="same")

    df = df[start:]
    print("doing regression")
    x, y = df["X_Value"], df["Tension_smooth"]
    c_2 = y[-500:].mean()
    y_shifted = y - c_2
    mask = y_shifted > 0
    x_lin = x[mask]
    y_lin = y_shifted[mask]
    log_y = np.log(y_lin)
    coeffs = np.polyfit(x_lin, log_y, 1)
    slope, intercept = coeffs
    b_2 = -1 / slope
    a_2 = np.exp(intercept)

    def model(t, a, b, c):
        return (a) * np.exp(-(t / b)) + c

    def model2(t, b):
        return (y[start] - c_2) * np.exp(-(t / b)) + c_2

    # lower_bounds = [0, 0, 0]  # minimum values for a, b, c
    # upper_bounds = [1000000, 10, 0.01]
    params, pcov = curve_fit(
        model,
        x,
        y,
        p0=[a_2, b_2, c_2],
        maxfev=7000,
        # bounds=(lower_bounds, upper_bounds),
    )
    print(np.sqrt(np.diag(pcov)))
    params2 = a_2, params[0], c_2
    return params
