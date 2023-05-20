import numpy as np


def lagrange_interpolation(x, y):
    n = len(x)

    X_int = np.linspace(x[0], x[-1], 1000)
    Y_int = np.zeros(len(X_int))

    for i in range(len(X_int)):
        print(f"\rInterpolacja Lagrange'a: {round(i / len(X_int) * 100)}%", end="")
        for j in range(n):
            L = 1
            for k in range(n):
                if k != j:
                    L *= (X_int[i] - x[k]) / (x[j] - x[k])
            Y_int[i] += y[j] * L

    print("\rInterpolacja Lagrange'a: 100%")

    return X_int, Y_int


def third_degree_spline_interpolation(x, y):
    n = len(x)

    X_int = np.linspace(x[0], x[-1], 1000)
    Y_int = np.zeros(len(X_int))

    # TODO: Implementacja interpolacji funkcjami sklejanymi

    print("\rInterpolacja funkcjami sklejanymi: 100%")

    return X_int, Y_int
