from sqlalchemy.orm import Session

def resolve_id(session: Session, external_id: str, table):
    entity = session.query(table).filter_by(sf_id=external_id).first()
    if entity:
        return entity.id
    return None