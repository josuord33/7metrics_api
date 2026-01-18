from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from src.core.domain.enums import DefenseType, TeamSide, MatchStatus

class Match(BaseModel):
    """Domain Entity for a Match."""
    id: Optional[str] = None
    team_a_name: str
    team_b_name: str
    defense_a: DefenseType = DefenseType.SIX_ZERO
    defense_b: DefenseType = DefenseType.SIX_ZERO
    initial_possession: Optional[TeamSide] = None
    local_score: int = 0
    visitor_score: int = 0
    total_time_seconds: int = 0
    status: MatchStatus = MatchStatus.SETUP
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
