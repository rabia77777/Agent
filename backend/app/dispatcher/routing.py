from math import radians, cos, sin, asin, sqrt
from typing import Optional, Tuple

CITY_TO_COORDS = {
    "los angeles": (34.0522, -118.2437),
    "san francisco": (37.7749, -122.4194),
    "seattle": (47.6062, -122.3321),
    "portland": (45.5152, -122.6784),
    "phoenix": (33.4484, -112.0740),
    "denver": (39.7392, -104.9903),
    "dallas": (32.7767, -96.7970),
    "houston": (29.7604, -95.3698),
    "chicago": (41.8781, -87.6298),
    "atlanta": (33.7490, -84.3880),
    "miami": (25.7617, -80.1918),
    "new york": (40.7128, -74.0060),
}


def geocode_city(name: str) -> Optional[Tuple[float, float]]:
    key = name.strip().lower()
    if key in CITY_TO_COORDS:
        return CITY_TO_COORDS[key]
    # Try parsing as "lat,lon"
    try:
        parts = [float(p.strip()) for p in name.split(",")]
        if len(parts) == 2:
            return parts[0], parts[1]
    except Exception:
        pass
    return None


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    miles = 3956 * c
    return miles


def eta_hours_for_distance(distance_miles: float, average_speed_mph: float) -> float:
    if average_speed_mph <= 0:
        return 0.0
    return distance_miles / average_speed_mph