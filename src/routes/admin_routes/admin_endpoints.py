from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.common import admin
from src.db.database import get_db
from src.schema.admin_schema.schema import (
    Employee,
    Attendance,
    EmployeeCreate,
    AttendanceCreate,
    EmployeeUpdate,
)

router = APIRouter(tags=["admin"])


@router.get("/employees", response_model=List[Employee])
def read_employees(db: Session = Depends(get_db)):
    return admin.get_employees(db)


@router.post("/employees", response_model=Employee)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return admin.add_employee(db, employee)


@router.put("/employees/{employee_id}", response_model=Employee)
def update_employee_api(
    employee_id: str, employee: EmployeeUpdate, db: Session = Depends(get_db)
):
    return admin.update_employee(db, employee_id, employee)


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    return admin.delete_employee(db, employee_id)


@router.post("/attendance", response_model=Attendance)
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    return admin.mark_attendance(db, attendance)


@router.get("/attendance/present-today", response_model=List[Employee])
def get_present_employees(db: Session = Depends(get_db)):
    return admin.get_present_employees(db)


@router.get("/attendance/{employee_id}", response_model=List[Attendance])
def get_attendance(employee_id: str, db: Session = Depends(get_db)):
    return admin.get_attendance(db, employee_id)
