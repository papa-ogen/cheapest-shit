from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "Cheapest products possible"
    ROOT_PATH: str = "/api/v1"

settings = Settings()