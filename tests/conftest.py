import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.main import app
from src.infrastructure.config.settings import settings
from src.infrastructure.persistence.models.match_model import MatchModel
from src.infrastructure.persistence.models.event_model import EventModel
from src.infrastructure.persistence.models.player_model import PlayerModel

@pytest.fixture(scope="function")
async def test_db_client() -> AsyncIOMotorClient:
    """Create a MongoDB client for testing."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    # Use a separate test database
    db_name = "test_handball_statistics"
    await init_beanie(
        database=client[db_name],
        document_models=[MatchModel, EventModel, PlayerModel] # Added PlayerModel just in case
    )
    yield client
    # Clean up after test
    await client.drop_database(db_name)

@pytest.fixture(scope="function")
async def client(test_db_client) -> AsyncGenerator[AsyncClient, None]:
    """Create an AsyncClient for testing API endpoints."""
    # Initialize DB for each test function (though session fixture handles init_beanie)
    # We yield the client to make requests
    from httpx import ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    # Clean up collections after each test
    await MatchModel.delete_all()
    await EventModel.delete_all()
