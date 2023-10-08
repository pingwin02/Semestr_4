import numpy as np


def lagrange_interpolation(nodes):
    """
    Funkcja wykonuje interpolację Lagrange'a na podstawie węzłów interpolacji.

    Args:
        nodes (tuple): Para złożona z listy odległości i wysokości węzłów interpolacji.

    Returns:
        tuple: Para złożona z listy odległości i interpolowanych wartości wysokości.
    """
    x, y = nodes
    n = len(x)

    X_int = np.linspace(x[0], x[-1], 1000)
    Y_int = np.zeros(len(X_int))

    for i in range(len(X_int)):
        print(f"\rInterpolacja Lagrange'a: {round(i / len(X_int) * 100)}%", end="")
        for j in range(n):
            fi = 1
            for k in range(n):
                if k != j:
                    fi *= (X_int[i] - x[k]) / (x[j] - x[k])
            Y_int[i] += y[j] * fi

    print("\rInterpolacja Lagrange'a: 100%")

    return X_int, Y_int


def third_degree_spline_interpolation(nodes):
    """
    Funkcja wykonuje interpolację funkcjami sklejanymi 3. stopnia na podstawie węzłów interpolacji.

    Args:
        nodes (tuple): Para złożona z listy odległości i wysokości węzłów interpolacji.

    Returns:
        tuple: Para złożona z listy odległości i interpolowanych wartości wysokości.
    """
    x, y = nodes

    n = len(x) - 1

    X_int = np.linspace(x[0], x[-1], 1000)
    Y_int = np.zeros(len(X_int))

    A = np.zeros((4 * n, 4 * n))
    b = np.zeros(((4 * n), 1))

    print("\rInterpolacja funkcjami sklejanymi: 0%", end="")

    # Równania a_i = f(x_i)
    for i in range(n):
        A[i][4 * i] = 1
        b[i] = y[i]

    # Równania a_i + b_i*h + c_i*h^2 + d_i*h^3 = f(x_i+1)
    j = 0
    for i in range(n, 2 * n):
        h = x[j + 1] - x[j]
        A[i][4 * j] = 1
        A[i][4 * j + 1] = h
        A[i][4 * j + 2] = h ** 2
        A[i][4 * j + 3] = h ** 3
        b[i] = y[j + 1]
        j += 1

    # Równania b_i + 2*c_i*h + 3*d_i*h^2 = b_i+1
    j = 0
    for i in range(2 * n, 3 * n - 1):
        h = x[j + 1] - x[j]
        A[i][4 * j + 1] = 1
        A[i][4 * j + 2] = 2 * h
        A[i][4 * j + 3] = 3 * h ** 2
        A[i][4 * j + 5] = -1
        b[i] = 0
        j += 1

    # Równania 2*c_i + 6*d_i*h = 2*c_i+1
    j = 0
    for i in range(3 * n - 1, 4 * n - 2):
        h = x[j + 1] - x[j]
        A[i][4 * j + 2] = 2
        A[i][4 * j + 3] = 6 * h
        A[i][4 * j + 6] = -2
        b[i] = 0
        j += 1

    # Równanie c_0 = 0
    A[4 * n - 2][2] = 1
    b[4 * n - 2] = 0

    # Równanie 2*c_n + 6*d_n*h = 0
    h = x[n] - x[n - 1]
    A[4 * n - 1][4 * n - 2] = 2
    A[4 * n - 1][4 * n - 1] = 6 * h
    b[4 * n - 1] = 0

    # Rozwiązanie układu równań
    c = np.linalg.solve(A, b)

    # Wyznaczenie wartości funkcji interpolującej
    for i in range(len(X_int)):
        print(f"\rInterpolacja funkcjami sklejanymi: {round(i / len(X_int) * 100)}%", end="")
        for j in range(n):
            # Wyznaczenie przedziału, w którym znajduje się X_int[i]
            if x[j] <= X_int[i] <= x[j + 1]:
                h = X_int[i] - x[j]
                Y_int[i] = c[4 * j] + c[4 * j + 1] * h + c[4 * j + 2] * h ** 2 + c[4 * j + 3] * h ** 3
                break

    print("\rInterpolacja funkcjami sklejanymi: 100%")
    return X_int, Y_int
