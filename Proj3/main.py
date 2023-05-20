import os

import numpy as np
from matplotlib import pyplot as plt

from Proj3.interpolations import lagrange_interpolation, third_degree_spline_interpolation
from gpx_handler import parse_gpx_file


def plot_elevation_profile(data, nodes, int_data, route_name, interp_type):
    ele, dist = data
    X, Y = nodes
    X_int, Y_int = int_data
    plt.plot(dist, ele, "o", label="Dane rzeczywiste", markersize=4, color="gray")
    plt.plot(X, Y, "ro", label="Węzły interpolacji", markersize=2)
    plt.plot(X_int, Y_int, "b--", label=interp_type, linewidth=1)
    plt.xlabel("Odległość (km)")
    plt.ylabel("Wysokość (m)")
    plt.ylim(min(ele) - 20, max(ele) + 20)
    plt.title(route_name + ".png")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"plots/{route_name}.png")
    plt.show()


def get_nodes(data, K, random=False):
    elevations, distances = data

    # Wybierz K punktów interpolacji
    if len(elevations) > K:
        if random:
            idx = np.random.randint(1, len(elevations) - 2, K - 2)
            idx = np.append(idx, [0, len(elevations) - 1])
            idx = sorted(idx)
        else:
            idx = sorted(np.linspace(0, len(elevations) - 1, K, dtype=int))
        X = [distances[i] for i in idx]
        Y = [elevations[i] for i in idx]

    return X, Y


if __name__ == "__main__":
    NUM_OF_POINTS = [25, 50, 100]

    if not os.path.exists("plots"):
        os.makedirs("plots")

    if not os.path.exists("routes"):
        raise Exception("Brak folderu z trasami")

    for track in os.listdir("routes"):
        data, route_name = parse_gpx_file(track)
        for num in NUM_OF_POINTS:
            print(f"\nLiczba węzłów interpolacji: {num}")
            filename = f"{route_name}_K={num}_Lagrange"

            nodes = get_nodes(data, num, random=False)

            int_data = lagrange_interpolation(nodes[0], nodes[1])
            plot_elevation_profile(data, nodes, int_data, filename, "Interpolacja Lagrange'a")

            filename = f"{route_name}_K={num}_Splajn"

            int_data = third_degree_spline_interpolation(nodes[0], nodes[1])
            plot_elevation_profile(data, nodes, int_data, filename, "Interpolacja funkcjami sklejanymi 3. stopnia")
