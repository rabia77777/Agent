from datetime import datetime, timezone, timedelta
from .models import insert_many_if_empty


async def seed() -> None:
    drivers = [
        {
            "_id": "D1",
            "name": "Alice Johnson",
            "current_location": {"city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
            "status": "available",
            "hours_driven_today": 2.5,
            "on_duty_start": (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat(),
            "last_break_start": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        },
        {
            "_id": "D2",
            "name": "Bob Smith",
            "current_location": {"city": "San Francisco", "lat": 37.7749, "lon": -122.4194},
            "status": "on_duty",
            "hours_driven_today": 5.0,
            "on_duty_start": (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat(),
            "last_break_start": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        },
        {
            "_id": "D3",
            "name": "Carol Nguyen",
            "current_location": {"city": "Phoenix", "lat": 33.4484, "lon": -112.0740},
            "status": "off_duty",
            "hours_driven_today": 0.0,
        },
    ]

    loads = [
        {
            "_id": "L1001",
            "pickup": {"city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
            "dropoff": {"city": "San Francisco", "lat": 37.7749, "lon": -122.4194},
            "status": "unassigned",
            "customer_contact": {"name": "Acme Co.", "email": "logistics@acme.example"},
            "notes": "Fragile",
        },
        {
            "_id": "L1002",
            "pickup": {"city": "Phoenix", "lat": 33.4484, "lon": -112.0740},
            "dropoff": {"city": "Denver", "lat": 39.7392, "lon": -104.9903},
            "status": "unassigned",
        },
    ]

    await insert_many_if_empty("drivers", drivers)
    await insert_many_if_empty("loads", loads)
    await insert_many_if_empty("assignments", [])