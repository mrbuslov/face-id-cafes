from sqlalchemy.orm import Session
from .models import Organization, Department, Guest
from .schemas import (
    Organization as OrganizationSchema,
)
from src.utils import hash_password


def get_organization(db: Session, org_id: int):
    return db.query(Organization).filter(Organization.id == org_id).first()

def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Organization).offset(skip).limit(100).all()

def create_organization(db: Session, org: OrganizationSchema):
    db_org = Organization(
        email = org.email,
        title = org.title,
        description = org.description,
        is_active = org.is_active,
    )
    # add object to session
    db.add(db_org)
    # commit changes
    db.commit()
    # refresh it to get new generated id
    db.refresh(db_org)
    return db_org
