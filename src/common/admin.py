from sqlalchemy.orm import Session
from src.models.admin.admin_models import Employee, Attendance
from src.schema.admin_schema.schema import (
    EmployeeCreate,
    AttendanceCreate,
    EmployeeUpdate,
)
from fastapi import HTTPException
from datetime import date


def get_employees(db: Session):
    return db.query(Employee).order_by(Employee.created_at.desc()).all()


def add_employee(db: Session, employee: EmployeeCreate):
    # employee_id unique check
    if db.query(Employee).filter(Employee.employee_id == employee.employee_id).first():
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    # email unique check
    if db.query(Employee).filter(Employee.email == employee.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_employee = Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


def update_employee(db: Session, employee_id: str, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if employee.email:
        email_user = (
            db.query(Employee)
            .filter(
                Employee.email == employee.email, Employee.employee_id != employee_id
            )
            .first()
        )
        if email_user:
            raise HTTPException(
                status_code=400, detail="Email already registered with another employee"
            )

    # Safe dynamic update
    for key, value in employee.model_dump(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: str):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}


def mark_attendance(db: Session, attendance: AttendanceCreate):
    # Check if employee exists
    db_employee = (
        db.query(Employee)
        .filter(Employee.employee_id == attendance.employee_id)
        .first()
    )
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if attendance already marked for that day
    existing_attendance = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == attendance.employee_id,
            Attendance.date == attendance.date,
        )
        .first()
    )

    if existing_attendance:
        if existing_attendance.status == attendance.status:
            raise HTTPException(
                status_code=400, detail=f"Attendance already marked as {attendance.status} for this day"
            )
        
        # Update status if it's different
        existing_attendance.status = attendance.status
        db.commit()
        db.refresh(existing_attendance)
        return existing_attendance

    new_attendance = Attendance(**attendance.model_dump())
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance


def get_attendance(db: Session, employee_id: str):
    return db.query(Attendance).filter(Attendance.employee_id == employee_id).all()


def get_present_employees(db: Session):
    today = date.today()
    return (
        db.query(Employee)
        .join(Attendance, Employee.employee_id == Attendance.employee_id)
        .filter(Attendance.date == today, Attendance.status == "Present")
        .all()
    )
