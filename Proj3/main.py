import os
import numpy as np
from matplotlib import pyplot as plt

from Proj3.interpolations import lagrange_interpolation, third_degree_spline_interpolation
from gpx_handler import parse_gpx_file


def plot_elevation_profile(data, nodes, int_data, route_name, interp_type):
    """
    Funkcja generuje wykres profilu wysokościowego na podstawie danych rzeczywistych i interpolowanych.

    Args:
        data (tuple): Para złożona z listy wysokości i odległości.
        nodes (tuple): Para złożona z listy węzłów interpolacji.
        int_data (tuple): Para złożona z listy interpolowanych wartości wysokości i odległości.
        route_name (str): Nazwa trasy.
        interp_type (str): Typ interpolacji.

    Returns:
        None
    """
    ele, dist = data
    X, Y = nodes
    X_int, Y_int = int_data
    plt.plot(dist, ele, "o", label="Dane rzeczywiste", markersize=3, color="gray")
    plt.plot(X, Y, "ro", label="Węzły interpolacji", markersize=2)
    plt.plot(X_int, Y_int, "b--", label=interp_type, linewidth=1)
    plt.xlabel("Odległość (km)")
    plt.ylabel("Wysokość (m)")
    plt.ylim(min(ele) - 20, max(ele) + 20)
    plt.title(route_name)
    plt.grid(True)
    plt.legend()
    plt.savefig(f"plots/{route_name}.png")
    plt.show()


def get_nodes(data, K, random=False):
    """
    Funkcja wybiera węzły interpolacji na podstawie danych rzeczywistych.

    Args:
        data (tuple): Para złożona z listy wysokości i odległości.
        K (int): Liczba węzłów interpolacji.
        random (bool): Flaga określająca czy wybór węzłów ma być losowy.

    Returns:
        tuple: Para złożona z listy odległości i wysokości wybranych węzłów interpolacji.
    """
    elevations, distances = data

    if random is False:
        idx = sorted(np.linspace(0, len(elevations) - 1, K, dtype=int))

    else:
        # Ensure that first and last point are included
        idx = [0, len(elevations) - 1]
        while len(idx) < K:
            new_idx = np.random.randint(1, len(elevations) - 1)
            if new_idx not in idx:
                idx.append(new_idx)
        idx = sorted(idx)
    X = [distances[i] for i in idx]
    Y = [elevations[i] for i in idx]

    return X, Y


if __name__ == "__main__":
    # Liczba węzłów interpolacji
    NUM_OF_POINTS = [15, 30]

    if os.path.exists("plots"):
        for plot in os.listdir("plots"):
            os.remove(f"plots/{plot}")
    else:
        os.makedirs("plots")

    if not os.path.exists("routes"):
        raise Exception("Brak folderu z trasami")

    for track in os.listdir("routes"):
        data, route_name = parse_gpx_file(track)
        for num in NUM_OF_POINTS:
            print(f"\nLiczba węzłów interpolacji: {num}")

            nodes = get_nodes(data, num)

            int_data = lagrange_interpolation(nodes)
            plot_elevation_profile(data, nodes, int_data, f"{route_name}_K={num}_Lagrange", "Interpolacja Lagrange'a")

            int_data = third_degree_spline_interpolation(nodes)
            plot_elevation_profile(data, nodes, int_data, f"{route_name}_K={num}_Splajn",
                                   "Interpolacja splajnami 3. stopnia")

            nodes = get_nodes(data, num, random=True)

            int_data = lagrange_interpolation(nodes)
            plot_elevation_profile(data, nodes, int_data, f"{route_name}_K={num}_Lagrange_rand",
                                   "Interpolacja Lagrange'a")

            int_data = third_degree_spline_interpolation(nodes)
            plot_elevation_profile(data, nodes, int_data, f"{route_name}_K={num}_Splajn_rand",
                                   "Interpolacja splajnami 3. stopnia")
