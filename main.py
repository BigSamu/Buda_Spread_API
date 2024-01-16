import uvicorn
from fastapi import FastAPI


from api.api.v1 import api_router
from api.core import settings

# ******************************************************************************
# FASTAPI APP SETTINGS
# ******************************************************************************

app = FastAPI(
    title="Buda.com Spread API",
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
    docs_url="/api/docs",
    redoc_url=None,  # Set to None if you don't want to use ReDoc
)

# ******************************************************************************
# ROUTE SETTINGS
# ******************************************************************************

app.include_router(api_router, prefix=f"/{settings.API_URL_PREFIX}")

# ******************************************************************************
# RUN SETTINGS
# ******************************************************************************

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
