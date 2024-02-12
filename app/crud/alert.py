from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Alert
from app.schemas import AlertCreate, AlertUpdate

class CRUDAlert(CRUDBase[Alert, AlertCreate, AlertUpdate]):
    # Declare model specific CRUD operation methods.
    pass


alert = CRUDAlert(Alert)
