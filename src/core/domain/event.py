from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from src.core.domain.enums import (
    TeamSide, ActionType, CourtZone, DefenseType
)

class Event(BaseModel):
    """Domain Entity for an Event."""
    id: Optional[str] = None
    match_id: str
    timestamp: int
    time_formatted: str
    player: int
    team: TeamSide
    action: ActionType
    court_zone: Optional[CourtZone] = None
    goal_zone: Optional[int] = None
    defense_at_moment: Optional[DefenseType] = None
    context: Optional[List[str]] = None
    rival_goalkeeper: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
