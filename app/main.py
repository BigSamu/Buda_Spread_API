import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.v1 import api_router
from config import settings

# ******************************************************************************
# FASTAPI APP SETTINGS
# ******************************************************************************

app = FastAPI(
    title="Buda Spread API",
    description="This API is designed for Buda.com to calculate and manage the spread across various markets. Key features include:\n\n"
    "- Retrieving the spread of all markets in a single API call.\n"
    "- Managing a 'spread alert' system, enabling users to set and check spread thresholds.\n\n"
    "The system supports polling to determine if the current spread is above or below these thresholds.\n\n",
    version="1.0.0",
    contact={
        "name": "Samuel Valdes Gutierrez",
        "email": "valdesgutierrez@gmail.com",
        "github": "https://github.com/BigSamu",
    },
    terms_of_service="http://api.buda.com/terms/",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/api/docs",  # This is the default URL for the Swagger UI
    redoc_url="/api/redoc",  # This is the default URL for the ReDoc UI
)


# ******************************************************************************
# DATABASE SETTINGS (SUPPOSING NO MIGRATION TOOL (i.e ALEMBIC))
# ******************************************************************************

# Create tables in database.
from app.database.base import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

# ******************************************************************************
# ROUTE SETTINGS
# ******************************************************************************

app.include_router(api_router, prefix=f"/{settings.API_URL_PREFIX}")
