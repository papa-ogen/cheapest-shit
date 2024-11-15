import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from tortoise import Tortoise

load_dotenv()


class Settings(BaseModel):
    APP_NAME: str = "Cheapest products possible"
    ROOT_PATH: str = "/api/v1"
    OPENAI_API_PROJECT_NAME: Optional[str] = os.getenv("OPEN_API_PROJECT_NAME")
    OPENAI_API_ORGANIZATION: Optional[str] = os.getenv("OPEN_API_ORGANIZATION")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")


settings = Settings()

DATABASE_URL = "postgres://postgres:test@localhost:5432/cheapest_shit"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    # Initialize Tortoise ORM with configuration
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
