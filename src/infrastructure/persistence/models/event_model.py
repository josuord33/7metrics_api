from beanie import Document, PydanticObjectId
from datetime import datetime
from typing import Optional, List
from pydantic import Field
from src.core.domain.enums import TeamSide, ActionType, CourtZone, DefenseType

class EventModel(Document):
    match_id: PydanticObjectId
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

    class Settings:
        name = "events"
