from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class Location(BaseModel):
    city: Optional[str] = None
    lat: float
    lon: float


class Driver(BaseModel):
    id: str = Field(alias="_id")
    name: str
    current_location: Location
    status: Literal["available", "on_duty", "off_duty", "assigned"] = "available"
    hours_driven_today: float = 0.0
    on_duty_start: Optional[datetime] = None
    last_break_start: Optional[datetime] = None
    assigned_load_id: Optional[str] = None

    class Config:
        populate_by_name = True


class Load(BaseModel):
    id: str = Field(alias="_id")
    pickup: Location
    dropoff: Location
    status: Literal["unassigned", "assigned", "in_transit", "delivered"] = "unassigned"
    customer_contact: Optional[dict] = None
    notes: Optional[str] = None

    class Config:
        populate_by_name = True


class Assignment(BaseModel):
    id: str = Field(alias="_id")
    load_id: str
    driver_id: str
    assigned_at: datetime
    eta_hours: float
    distance_miles: float
    status: Literal["assigned", "in_transit", "delivered"] = "assigned"

    class Config:
        populate_by_name = True


# Requests
class AssignDriverRequest(BaseModel):
    load_id: str
    driver_id: Optional[str] = None


class AssignDriverResponse(BaseModel):
    assignment: Assignment
    driver: Driver
    load: Load
    hos_ok: bool
    hos_reason: Optional[str] = None


class RouteETARequest(BaseModel):
    origin: str
    destination: str


class RouteETAResponse(BaseModel):
    distance_miles: float
    eta_hours: float


class NotifyRequest(BaseModel):
    message: str
    load_id: Optional[str] = None
    driver_id: Optional[str] = None


class NotifyResponse(BaseModel):
    delivered: bool


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    action: str
    data: dict


class DriverStatusResponse(BaseModel):
    driver: Optional[Driver]


class DriversListResponse(BaseModel):
    drivers: List[Driver]


class LoadsListResponse(BaseModel):
    loads: List[Load]


class AssignmentsListResponse(BaseModel):
    assignments: List[Assignment]


class UpdateAssignmentStatusRequest(BaseModel):
    assignment_id: str
    status: Literal["assigned", "in_transit", "delivered"]


class UpdateAssignmentStatusResponse(BaseModel):
    assignment: Assignment