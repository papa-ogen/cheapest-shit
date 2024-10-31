import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_read_root() -> None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"app_name": "Cheapest products possible"}
