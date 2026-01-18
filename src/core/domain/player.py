from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from src.core.domain.enums import TeamSide, Position, Hand

class Player(BaseModel):
    """Domain Entity for a Player."""
    id: Optional[str] = None
    match_id: str
    team: TeamSide
    number: int
    name: str
    is_goalkeeper: bool = False
    position: Optional[Position] = None
    hand: Optional[Hand] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
