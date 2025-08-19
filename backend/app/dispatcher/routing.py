from math import radians, cos, sin, asin, sqrt
from typing import Optional, Tuple

CITY_TO_COORDS = {
    # Canada
    "toronto": (43.6532, -79.3832),
    "montreal": (45.5017, -73.5673),
    "vancouver": (49.2827, -123.1207),
    "calgary": (51.0447, -114.0719),
    "edmonton": (53.5461, -113.4938),
    "ottawa": (45.4215, -75.6972),
    "winnipeg": (49.8954, -97.1385),
    "quebec city": (46.8139, -71.2080),
    "halifax": (44.6488, -63.5752),
    "victoria": (48.4284, -123.3656),
    # Keep a few US cities to allow cross-border demos if needed
    "seattle": (47.6062, -122.3321),
    "portland": (45.5152, -122.6784),
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