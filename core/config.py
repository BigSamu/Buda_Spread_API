import secrets
from typing import Optional

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # PATH SETTINGS
    API_URL_PREFIX: str = "https://www.buda.com/api/v2"

    class Config:
        env_file = ".env"


settings = Settings()
