from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Alert(Base):
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Alert id={self.id} value={self.value}>"
