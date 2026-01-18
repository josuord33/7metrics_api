from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional
from src.core.domain.enums import DefenseType, TeamSide, MatchStatus

class MatchModel(Document):
    team_a_name: str
    team_b_name: str
    defense_a: DefenseType
    defense_b: DefenseType
    initial_possession: Optional[TeamSide] = None
    local_score: int = 0
    visitor_score: int = 0
    total_time_seconds: int = 0
    status: MatchStatus = MatchStatus.SETUP
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "matches"
