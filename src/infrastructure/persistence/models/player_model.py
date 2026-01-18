from beanie import Document, PydanticObjectId, Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime
from src.core.domain.enums import TeamSide, Position, Hand

class PlayerModel(Document):
    match_id: Indexed(PydanticObjectId)
    team: TeamSide
    number: int
    name: str
    is_goalkeeper: bool = False
    position: Optional[Position] = None
    hand: Optional[Hand] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "players"
        indexes = [
            "match_id",
            [("match_id", 1), ("team", 1), ("number", 1)],
        ]
