from typing import Optional
from ..realtime.websocket import manager


async def notify_all(event: str, payload: dict) -> None:
    await manager.broadcast({"event": event, "payload": payload})


async def notify_assignment(load_id: str, driver_id: str, eta_hours: float, distance_miles: float) -> None:
    await notify_all(
        "assignment",
        {
            "load_id": load_id,
            "driver_id": driver_id,
            "eta_hours": eta_hours,
            "distance_miles": distance_miles,
        },
    )


async def notify_message(message: str, load_id: Optional[str] = None, driver_id: Optional[str] = None) -> None:
    await notify_all(
        "notification",
        {
            "message": message,
            "load_id": load_id,
            "driver_id": driver_id,
        },
    )