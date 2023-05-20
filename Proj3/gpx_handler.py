import math
import xml.etree.ElementTree as ET


def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    return distance


def parse_gpx_file(file_path):
    file_path = "routes/" + file_path
    tree = ET.parse(file_path)
    root = tree.getroot()

    elevations = []
    distances = [0]
    X = []
    Y = []
    prev_lat = None
    prev_lon = None
    total_distance = 0
    route_name = root.find("{http://www.topografix.com/GPX/1/1}trk").find(
        "{http://www.topografix.com/GPX/1/1}name").text

    for trkpt in root.iter("{http://www.topografix.com/GPX/1/1}trkpt"):
        lat = float(trkpt.attrib["lat"])
        lon = float(trkpt.attrib["lon"])
        ele = float(trkpt.find("{http://www.topografix.com/GPX/1/1}ele").text)

        if prev_lat is not None and prev_lon is not None:
            distance = calculate_distance(prev_lat, prev_lon, lat, lon)
            total_distance += distance
            distances.append(total_distance)

        elevations.append(ele)
        prev_lat = lat
        prev_lon = lon

    print(f"Trasa: {route_name}")
    print(f"Dystans: {total_distance:.3f} km")
    print(f"Ilość punktów danych: {len(elevations)}")

    return (elevations, distances), route_name
