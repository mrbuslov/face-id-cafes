# SQLAlchemy models

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    is_active = Column(Boolean, default=True)

    departments = relationship('Department', back_populates='organization')
    # every organization should have own guests. They don't have to be used by other orgs.
    guests = relationship('Guest', back_populates='organization')


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    hashed_password = Column(String) # we assume, that people will login with department account

    organization = relationship('Organization', back_populates='departments')
    orders = relationship('Order', back_populates='department')


class Guest(Base):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True, index=True)

    organization = relationship('Organization', back_populates='guests')