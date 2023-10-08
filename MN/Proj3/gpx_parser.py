import math
import xml.etree.ElementTree as ET

from matplotlib import pyplot as plt


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Funkcja oblicza odległość między dwoma punktami na sferze o zadanych współrzędnych geograficznych.
    Wykorzystuje wzór haversine.

    Args:
        lat1 (float): Szerokość geograficzna pierwszego punktu w stopniach.
        lon1 (float): Długość geograficzna pierwszego punktu w stopniach.
        lat2 (float): Szerokość geograficzna drugiego punktu w stopniach.
        lon2 (float): Długość geograficzna drugiego punktu w stopniach.

    Returns:
        float: Odległość między punktami w kilometrach.
    """
    earth_radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    return distance


def parse_gpx_file(file_path):
    """
    Funkcja parsuje plik GPX zawierający trasę i zwraca dane dotyczące profilu wysokościowego.

    Args:
        file_path (str): Ścieżka do pliku GPX.

    Returns:
        tuple: Para złożona z listy wysokości i odległości oraz nazwy trasy.
    """
    file_path = "routes/" + file_path
    tree = ET.parse(file_path)
    root = tree.getroot()

    elevations = []  # Lista wysokości
    distances = [0]  # Lista odległości, zaczynamy od 0
    prev_lat = None
    prev_lon = None
    total_distance = 0  # Całkowita odległość
    route_name = root.find("{http://www.topografix.com/GPX/1/1}trk").find(
        "{http://www.topografix.com/GPX/1/1}name").text  # Nazwa trasy

    for trkpt in root.iter("{http://www.topografix.com/GPX/1/1}trkpt"):
        lat = float(trkpt.attrib["lat"])  # Szerokość geograficzna punktu
        lon = float(trkpt.attrib["lon"])  # Długość geograficzna punktu
        ele = float(trkpt.find("{http://www.topografix.com/GPX/1/1}ele").text)  # Wysokość punktu

        if prev_lat is not None and prev_lon is not None:
            # Obliczanie odległości między kolejnymi punktami
            distance = calculate_distance(prev_lat, prev_lon, lat, lon)
            total_distance += distance
            distances.append(total_distance)

        elevations.append(ele)  # Dodanie wysokości do listy
        prev_lat = lat
        prev_lon = lon

    plt.figure(figsize=(15, 5))
    plt.scatter(distances, elevations, c=elevations, cmap="viridis", s=3)
    plt.xlabel("Odległość (km)")
    plt.ylabel("Wysokość (m)")
    plt.grid(True)
    plt.title(f"{route_name} - profil wysokościowy")
    plt.savefig(f"routes/{route_name}_profile.png")
    # plt.show()
    plt.close()

    print(f"\nTrasa: {route_name}")
    print(f"Dystans: {total_distance:.3f} km")
    print(f"Różnica wysokości: {max(elevations) - min(elevations):.3f} m")
    print(f"Ilość punktów danych: {len(elevations)}")

    return (elevations, distances), route_name
