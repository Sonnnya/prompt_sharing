import pytest
import pytest_asyncio
from tortoise import Tortoise

from app.server.server import app
from tests.utils import client_manager, ClientManagerType


@pytest_asyncio.fixture(scope="function")
async def async_client() -> ClientManagerType:
    async with client_manager(app) as c:
        yield c


@pytest.fixture(scope="function")
def anyio_backend() -> str:
    return "asyncio"


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db():
    """
    Фикстура для очистки базы данных перед каждым тестом, чтобы тесты были независимыми.
    """
    for model in Tortoise.apps.get("models", {}).values():
        await model.all().delete()
    yield
