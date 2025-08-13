from fastapi import APIRouter, HTTPException
from ..schemas import (
    AssignDriverRequest,
    AssignDriverResponse,
    RouteETARequest,
    RouteETAResponse,
    NotifyRequest,
    NotifyResponse,
    DriverStatusResponse,
)
from ..dispatcher.ai_dispatcher import dispatcher
from ..models import get_driver_by_id
from ..dispatcher.notifier import notify_message

router = APIRouter(prefix="/api")


@router.post("/assign_driver", response_model=dict)
async def assign_driver(req: AssignDriverRequest):
    result = await dispatcher.assign_driver(load_id=req.load_id, driver_id=req.driver_id, nearest=(req.driver_id is None))
    if "error" in result.get("data", {}):
        raise HTTPException(status_code=400, detail=result["data"])
    return result


@router.post("/route_eta", response_model=RouteETAResponse)
async def route_eta(req: RouteETARequest):
    result = await dispatcher.route_eta(req.origin, req.destination)
    data = result.get("data", {})
    if "error" in data:
        raise HTTPException(status_code=400, detail=data)
    return data


@router.get("/drivers/{driver_id}/status", response_model=DriverStatusResponse)
async def get_driver_status(driver_id: str):
    driver = await get_driver_by_id(driver_id)
    return {"driver": driver}


@router.get("/get_driver_status", response_model=DriverStatusResponse)
async def get_driver_status_alias(driver_id: str):
    driver = await get_driver_by_id(driver_id)
    return {"driver": driver}


@router.post("/notify", response_model=NotifyResponse)
async def notify(req: NotifyRequest):
    await notify_message(req.message, load_id=req.load_id, driver_id=req.driver_id)
    return {"delivered": True}