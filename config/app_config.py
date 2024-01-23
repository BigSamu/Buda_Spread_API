from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # PATH SETTINGS
    API_URL_PREFIX: str = "api/v1"
    BUDA_API_URL: str = "https://www.buda.com/api/v2"

    class ConfigDict:
        env_file = ".env"

settings = Settings()
