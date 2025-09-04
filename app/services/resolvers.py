from sqlalchemy.orm import Session
from models.staff import Staff

def resolve_staff_id(session: Session, external_id: str):
    staff = session.query(Staff).filter_by(sf_id=external_id).first()
    if staff:
        return staff.id
    return None