from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from .db import get_collection


async def list_available_drivers() -> List[Dict[str, Any]]:
    drivers = get_collection("drivers")
    cursor = drivers.find({"status": {"$in": ["available", "on_duty"]}})
    return [doc async for doc in cursor]


async def get_driver_by_id(driver_id: str) -> Optional[Dict[str, Any]]:
    drivers = get_collection("drivers")
    return await drivers.find_one({"_id": driver_id})


async def set_driver_assigned(driver_id: str, load_id: str) -> None:
    drivers = get_collection("drivers")
    await drivers.update_one(
        {"_id": driver_id},
        {"$set": {"status": "assigned", "assigned_load_id": load_id}},
    )


async def update_driver_status(driver_id: str, status: str) -> None:
    drivers = get_collection("drivers")
    await drivers.update_one({"_id": driver_id}, {"$set": {"status": status}})


async def get_load_by_id(load_id: str) -> Optional[Dict[str, Any]]:
    loads = get_collection("loads")
    return await loads.find_one({"_id": load_id})


async def set_load_assigned(load_id: str) -> None:
    loads = get_collection("loads")
    await loads.update_one({"_id": load_id}, {"$set": {"status": "assigned"}})


async def create_assignment(load_id: str, driver_id: str, eta_hours: float, distance_miles: float) -> Dict[str, Any]:
    assignments = get_collection("assignments")
    assignment = {
        "_id": f"A{int(datetime.now(timezone.utc).timestamp())}",
        "load_id": load_id,
        "driver_id": driver_id,
        "assigned_at": datetime.now(timezone.utc).isoformat(),
        "eta_hours": float(eta_hours),
        "distance_miles": float(distance_miles),
        "status": "assigned",
    }
    await assignments.insert_one(assignment)
    return assignment


async def insert_many_if_empty(collection_name: str, documents: List[Dict[str, Any]]) -> None:
    collection = get_collection(collection_name)
    count = await collection.count_documents({})
    if count == 0 and documents:
        await collection.insert_many(documents)