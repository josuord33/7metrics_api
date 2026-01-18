from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.infrastructure.config.settings import settings
from src.infrastructure.persistence.models.match_model import MatchModel
from src.infrastructure.persistence.models.event_model import EventModel
from src.infrastructure.persistence.models.player_model import PlayerModel
from src.infrastructure.api.routers import matches, events, players, statistics

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[MatchModel, EventModel, PlayerModel]
    )
    print("✅ Database connected successfully!")
    yield
    print("👋 Application shutting down...")

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan
)

app.include_router(matches.router)
app.include_router(players.router)
app.include_router(events.router)
app.include_router(statistics.router)

@app.get("/")
async def root():
    return {"message": "Welcome to 7metrics API"}
