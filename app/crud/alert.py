from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Alert
from app.schemas import AlertResponse

class CRUDAlert(CRUDBase[Alert, AlertCreate, AlertUpdate]):
    # Declare model specific CRUD operation methods.

    def get_one_by_name(self, db: Session, name: str) -> Alert:
        return db.query(Alert).filter(Alert.name == name).first()


company = CRUDAlert(Alert)
