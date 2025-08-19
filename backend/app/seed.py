from datetime import datetime, timezone, timedelta
from .models import insert_many_if_empty


async def seed() -> None:
    # Canadian demo data
    drivers = [
        {
            "_id": "D1",
            "name": "Ava Martin",
            "current_location": {"city": "Toronto", "lat": 43.6532, "lon": -79.3832},
            "status": "available",
            "hours_driven_today": 1.5,
            "on_duty_start": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "last_break_start": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        },
        {
            "_id": "D2",
            "name": "Liam Roy",
            "current_location": {"city": "Montreal", "lat": 45.5017, "lon": -73.5673},
            "status": "available",
            "hours_driven_today": 0.5,
            "on_duty_start": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "last_break_start": (datetime.now(timezone.utc) - timedelta(hours=0.5)).isoformat(),
        },
        {
            "_id": "D3",
            "name": "Noah Singh",
            "current_location": {"city": "Calgary", "lat": 51.0447, "lon": -114.0719},
            "status": "on_duty",
            "hours_driven_today": 4.0,
            "on_duty_start": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
            "last_break_start": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        },
    ]

    loads = [
        {
            "_id": "L2001",
            "pickup": {"city": "Toronto", "lat": 43.6532, "lon": -79.3832},
            "dropoff": {"city": "Montreal", "lat": 45.5017, "lon": -73.5673},
            "status": "unassigned",
            "customer_contact": {"name": "Maple Foods", "email": "ops@maplefoods.example"},
            "notes": "Refrigerated",
        },
        {
            "_id": "L2002",
            "pickup": {"city": "Vancouver", "lat": 49.2827, "lon": -123.1207},
            "dropoff": {"city": "Calgary", "lat": 51.0447, "lon": -114.0719},
            "status": "unassigned",
        },
        {
            "_id": "L2003",
            "pickup": {"city": "Ottawa", "lat": 45.4215, "lon": -75.6972},
            "dropoff": {"city": "Toronto", "lat": 43.6532, "lon": -79.3832},
            "status": "unassigned",
        },
        {
            "_id": "L2004",
            "pickup": {"city": "Edmonton", "lat": 53.5461, "lon": -113.4938},
            "dropoff": {"city": "Winnipeg", "lat": 49.8954, "lon": -97.1385},
            "status": "unassigned",
        },
        {
            "_id": "L2005",
            "pickup": {"city": "Quebec City", "lat": 46.8139, "lon": -71.2080},
            "dropoff": {"city": "Halifax", "lat": 44.6488, "lon": -63.5752},
            "status": "unassigned",
        },
        {
            "_id": "L2006",
            "pickup": {"city": "Victoria", "lat": 48.4284, "lon": -123.3656},
            "dropoff": {"city": "Vancouver", "lat": 49.2827, "lon": -123.1207},
            "status": "unassigned",
        },
        {
            "_id": "L2007",
            "pickup": {"city": "Montreal", "lat": 45.5017, "lon": -73.5673},
            "dropoff": {"city": "Quebec City", "lat": 46.8139, "lon": -71.2080},
            "status": "unassigned",
        },
        {
            "_id": "L2008",
            "pickup": {"city": "Toronto", "lat": 43.6532, "lon": -79.3832},
            "dropoff": {"city": "Ottawa", "lat": 45.4215, "lon": -75.6972},
            "status": "unassigned",
        },
    ]

    await insert_many_if_empty("drivers", drivers)
    await insert_many_if_empty("loads", loads)
    await insert_many_if_empty("assignments", [])