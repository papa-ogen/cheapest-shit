from fastapi import FastAPI

app = FastAPI()

ROOT_PATH = "/api"

@app.get(f"{ROOT_PATH}/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}