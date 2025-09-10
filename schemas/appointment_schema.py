from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime, date


class AppointmentBase(BaseModel):
    center_id: UUID
    provider_id: UUID
    service_id: UUID
    status: str
    notes: Optional[str] = None
    scheduled_time: datetime              # ✅ unified name
    guest_id: UUID
    appointment_date: Optional[date] = None

    @field_validator("appointment_date", mode="before")
    def set_appointment_date(cls, v, values):
        """Auto-fill appointment_date from scheduled_time if not provided"""
        if v is None and "scheduled_time" in values and values["scheduled_time"]:
            return values["scheduled_time"].date()
        return v


class AppointmentCreate(AppointmentBase):
    pass  # no extra fields needed


class AppointmentRead(AppointmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   # ✅ SQLAlchemy -> Pydantic mapping


class AppointmentResponse(AppointmentRead):
    message: str


class AppointmentOut(BaseModel):
    id: UUID
    guest_id: UUID
    center_id: UUID
    service_id: UUID
    scheduled_time: datetime             # ✅ consistent
    created_at: datetime


class AppointmentUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    appointment_date: Optional[date] = None

    @field_validator("appointment_date", mode="before")
    def set_appointment_date(cls, v, values):
        """Auto-update appointment_date if only scheduled_time is given"""
        if v is None and "scheduled_time" in values and values["scheduled_time"]:
            return values["scheduled_time"].date()
        return v
