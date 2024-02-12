from typing import Generator

from app.database import Session
# *******************************************************************************
# SESSION DATABASE DEPENDENCY
# *******************************************************************************


def get_db() -> Generator:
    # Create session while connection to database
    try:
        db = Session()
        yield db
    # Once finish close database session
    finally:
        db.close()
