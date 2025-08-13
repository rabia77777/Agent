import re
from typing import Dict, Any, Optional, Tuple
from ..config import settings
from .routing import geocode_city, haversine_miles, eta_hours_for_distance
from ..models import (
    list_available_drivers,
    get_driver_by_id,
    get_load_by_id,
    set_driver_assigned,
    set_load_assigned,
    create_assignment,
)
from .hos_rules import is_driver_hos_compliant
from .notifier import notify_assignment, notify_message


class Dispatcher:
    async def handle_message(self, message: str) -> Dict[str, Any]:
        msg = message.strip().lower()

        # assign load L1001 to nearest/driver D1
        m_assign = re.search(r"assign\s+load\s+(?P<load>L\w+)\s+(?:to\s+(?:(?:driver\s+(?P<driver>D\w+))|(?P<nearest>nearest)))?", msg)
        if m_assign:
            load_id = m_assign.group("load").upper()
            driver_id = m_assign.group("driver")
            nearest = m_assign.group("nearest") is not None
            return await self.assign_driver(load_id=load_id, driver_id=(driver_id.upper() if driver_id else None), nearest=nearest)

        # eta from X to Y
        m_eta = re.search(r"eta\s+from\s+(?P<origin>.+?)\s+to\s+(?P<dest>.+)$", msg)
        if m_eta:
            origin = m_eta.group("origin").strip()
            dest = m_eta.group("dest").strip()
            return await self.route_eta(origin, dest)

        # status of driver D1
        m_status = re.search(r"status\s+of\s+driver\s+(?P<driver>D\w+)", msg)
        if m_status:
            driver_id = m_status.group("driver").upper()
            driver = await get_driver_by_id(driver_id)
            return {"action": "get_driver_status", "data": {"driver": driver}}

        # notify customer for load L1001: some message
        m_notify = re.search(r"notify\s+customer\s+for\s+load\s+(?P<load>L\w+)\s*:\s*(?P<note>.+)$", msg)
        if m_notify:
            load_id = m_notify.group("load").upper()
            note = m_notify.group("note").strip()
            await notify_message(note, load_id=load_id)
            return {"action": "notify", "data": {"delivered": True}}

        return {"action": "unknown", "data": {"message": "could not parse"}}

    async def route_eta(self, origin: str, destination: str) -> Dict[str, Any]:
        o = geocode_city(origin)
        d = geocode_city(destination)
        if not o or not d:
            return {"action": "route_eta", "data": {"error": "unknown origin/destination"}}
        distance = haversine_miles(o[0], o[1], d[0], d[1])
        eta = eta_hours_for_distance(distance, settings.average_speed_mph)
        return {"action": "route_eta", "data": {"distance_miles": round(distance, 2), "eta_hours": round(eta, 2)}}

    async def assign_driver(self, load_id: str, driver_id: Optional[str], nearest: bool) -> Dict[str, Any]:
        load = await get_load_by_id(load_id)
        if not load:
            return {"action": "assign_driver", "data": {"error": "load not found"}}

        if driver_id:
            driver = await get_driver_by_id(driver_id)
            if not driver:
                return {"action": "assign_driver", "data": {"error": "driver not found"}}
        else:
            candidates = await list_available_drivers()
            driver = None
            if nearest and candidates:
                # choose driver nearest to pickup
                pickup = load.get("pickup")
                if pickup:
                    best = None
                    best_dist = 1e12
                    for d in candidates:
                        loc = d.get("current_location")
                        if loc and pickup:
                            dist = haversine_miles(loc["lat"], loc["lon"], pickup["lat"], pickup["lon"])  # type: ignore
                            if dist < best_dist:
                                best_dist = dist
                                best = d
                    driver = best
            if driver is None and candidates:
                driver = candidates[0]
            if driver is None:
                return {"action": "assign_driver", "data": {"error": "no available drivers"}}

        # compute distance and ETA pickup->dropoff
        pickup = load.get("pickup")
        dropoff = load.get("dropoff")
        distance = haversine_miles(pickup["lat"], pickup["lon"], dropoff["lat"], dropoff["lon"])  # type: ignore
        eta = eta_hours_for_distance(distance, settings.average_speed_mph)

        hos_ok, hos_reason = is_driver_hos_compliant(driver, eta)
        if not hos_ok:
            return {"action": "assign_driver", "data": {"error": "HOS violation", "hos_reason": hos_reason}}

        await set_driver_assigned(driver["_id"], load_id)
        await set_load_assigned(load_id)
        assignment = await create_assignment(load_id, driver["_id"], eta, distance)
        await notify_assignment(load_id, driver["_id"], eta, distance)

        return {
            "action": "assign_driver",
            "data": {
                "assignment": assignment,
                "driver": driver,
                "load": load,
                "hos_ok": True,
            },
        }


dispatcher = Dispatcher()