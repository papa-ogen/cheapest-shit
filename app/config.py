import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    APP_NAME: str = "Cheapest products possible"
    ROOT_PATH: str = "/api/v1"
    OPENAI_API_PROJECT_NAME: Optional[str] = os.getenv("OPEN_API_PROJECT_NAME")
    OPENAI_API_ORGANIZATION: Optional[str] = os.getenv("OPEN_API_ORGANIZATION")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")


settings = Settings()
