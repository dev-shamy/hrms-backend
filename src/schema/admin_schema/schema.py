from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from uuid import UUID


class EmployeeBase(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    department: Optional[str] = None


class AttendanceBase(BaseModel):
    employee_id: str
    date: date
    status: str


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    id: UUID

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    role: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class AdminLoginRequest(BaseModel):
    username: str
    password: str
