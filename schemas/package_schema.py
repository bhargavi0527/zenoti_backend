from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import date


class PackageBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
    active: Optional[bool] = True
    category_id: Optional[uuid.UUID] = None
    business_unit_id: Optional[uuid.UUID] = None
    version_id: Optional[uuid.UUID] = None
    time: Optional[int] = None
    booking_start_date: Optional[date] = None
    booking_end_date: Optional[date] = None
    commission_eligible: Optional[bool] = False
    commission_factor: Optional[float] = None
    commission_type: Optional[str] = None
    commission_value: Optional[float] = None
    series_package_type: Optional[str] = None
    series_package_cost_to_center: Optional[float] = None
    tags: Optional[str] = None
    center_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = True
    dq_check_remark: Optional[str] = None


class PackageCreate(PackageBase):
    pass


class PackageUpdate(PackageBase):
    pass


class PackageResponse(PackageBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
