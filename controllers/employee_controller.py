from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from services import employee_service
from schemas.employee_schema import EmployeeCreate, EmployeeUpdate, EmployeeOut
from typing import List
import uuid

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeOut)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.create_employee(db, employee)


@router.get("/", response_model=List[EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    return employee_service.get_all_employees(db)


@router.get("/{emp_id}", response_model=EmployeeOut)
def get_employee(emp_id: uuid.UUID, db: Session = Depends(get_db)):
    emp = employee_service.get_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.put("/{emp_id}", response_model=EmployeeOut)
def update_employee(emp_id: uuid.UUID, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    emp = employee_service.update_employee(db, emp_id, employee)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.delete("/{emp_id}")
def delete_employee(emp_id: uuid.UUID, db: Session = Depends(get_db)):
    emp = employee_service.delete_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}
