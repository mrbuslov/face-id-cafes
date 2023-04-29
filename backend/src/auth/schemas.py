# Pydantic models
from pydantic import BaseModel
from src.orders.schemas import Order


# --- Department ---
class DepartmentBase(BaseModel):
    pass


class DepartmentCreate(DepartmentBase):
    password: str


class Department(DepartmentBase):
    id: int
    organization_id: int
    orders: list[Order] = []

    class Config:
        orm_mode = True


# --- Guest ---
class GuestBase(BaseModel):
    pass


class GuestCreate(GuestBase):
    pass


class Guest(GuestBase):
    id: int
    organization_id: int

    class Config:
        orm_mode = True


# --- Organization ---
class OrganizationBase(BaseModel):
    email: str
    title: str
    description: str
    is_active: bool


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: int
    departments: list[Department] = []
    guests: list[Guest] = []

    class Config:
        orm_mode = True
