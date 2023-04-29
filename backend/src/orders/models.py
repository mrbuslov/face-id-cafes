# SQLAlchemy models

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Numeric
from sqlalchemy.orm import relationship
from src.database import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship('Department', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float(precision=2))
    quantity = Column(Float(precision=3))
    order_id = Column(Integer, ForeignKey("orders.id"))

    order = relationship('Order', back_populates='items')
