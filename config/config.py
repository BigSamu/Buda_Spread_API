from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PATH SETTINGS
    API_URL_PREFIX: str = "api/v1"
    BUDA_API_URL: str = "https://www.buda.com/api/v2"

    # Environment variables
    BUDA_API_SECRET: Optional[str] = None
    BUDA_API_KEY: Optional[str] = None

    class ConfigDict:
        env_file = ".env"


settings = Settings()
