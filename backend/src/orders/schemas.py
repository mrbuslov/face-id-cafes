# Pydantic models
from pydantic import BaseModel
import datetime


# --- Item ---
class ItemBase(BaseModel):
    name: str
    price: float
    quantity: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True


# --- Order ---
class OrderBase(BaseModel):
    created_at: datetime


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    department_id: int
    items: list[Item] = []

    class Config:
        orm_mode = True
