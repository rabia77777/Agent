from fastapi import APIRouter, HTTPException
from ..schemas import (
    AssignDriverRequest,
    AssignDriverResponse,
    RouteETARequest,
    RouteETAResponse,
    NotifyRequest,
    NotifyResponse,
    DriverStatusResponse,
    DriversListResponse,
    LoadsListResponse,
    AssignmentsListResponse,
    UpdateAssignmentStatusRequest,
    UpdateAssignmentStatusResponse,
)
from ..dispatcher.ai_dispatcher import dispatcher
from ..models import (
    get_driver_by_id,
    list_all_drivers,
    list_all_loads,
    list_all_assignments,
    update_assignment_status,
    set_driver_available,
    set_load_status,
)
from ..dispatcher.notifier import notify_message, notify_all
from ..seed import seed

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


@router.post("/reseed", response_model=dict)
async def reseed():
    await seed()
    return {"ok": True}


@router.get("/drivers", response_model=DriversListResponse)
async def list_drivers():
    return {"drivers": await list_all_drivers()}


@router.get("/loads", response_model=LoadsListResponse)
async def list_loads():
    return {"loads": await list_all_loads()}


@router.get("/assignments", response_model=AssignmentsListResponse)
async def list_assignments():
    return {"assignments": await list_all_assignments()}


@router.post("/assignments/status", response_model=UpdateAssignmentStatusResponse)
async def post_assignment_status(req: UpdateAssignmentStatusRequest):
    updated = await update_assignment_status(req.assignment_id, req.status)
    if not updated:
        raise HTTPException(status_code=404, detail={"error": "assignment not found"})
    # Cascade typical state changes for demo UX
    if req.status == "in_transit":
        await set_load_status(updated["load_id"], "in_transit")
    if req.status == "delivered":
        await set_load_status(updated["load_id"], "delivered")
        await set_driver_available(updated["driver_id"]) 
    await notify_all("assignment_updated", {"assignment": updated})
    return {"assignment": updated}