from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
import uuid


class EmployeeBase(BaseModel):
    employee_code: str
    name: str
    job_code: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    center_code: Optional[str] = None
    zone: Optional[str] = None

    is_active: Optional[bool] = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
