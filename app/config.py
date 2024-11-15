from pydantic import BaseModel
from tortoise import Tortoise


class Settings(BaseModel):
    APP_NAME: str = "Cheapest products possible"
    ROOT_PATH: str = "/api/v1"


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
