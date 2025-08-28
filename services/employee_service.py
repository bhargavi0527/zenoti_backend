from sqlalchemy.orm import Session
from models.employee import Employee
from schemas.employee_schema import EmployeeCreate, EmployeeUpdate
import uuid


def create_employee(db: Session, employee: EmployeeCreate):
    new_emp = Employee(**employee.dict())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


def get_all_employees(db: Session):
    return db.query(Employee).all()


def get_employee(db: Session, emp_id: uuid.UUID):
    return db.query(Employee).filter(Employee.id == emp_id).first()


def update_employee(db: Session, emp_id: uuid.UUID, emp_update: EmployeeUpdate):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        return None
    for key, value in emp_update.dict(exclude_unset=True).items():
        setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp


def delete_employee(db: Session, emp_id: uuid.UUID):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if emp:
        db.delete(emp)
        db.commit()
    return emp
