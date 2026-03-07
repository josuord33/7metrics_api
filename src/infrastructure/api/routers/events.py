from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from src.core.domain.event import Event
from src.core.domain.match import Match
from src.core.domain.enums import ActionType, CourtZone, DefenseType
from src.infrastructure.persistence.repositories.mongo_match_repository import MongoMatchRepository
from src.infrastructure.persistence.repositories.mongo_event_repository import MongoEventRepository
from src.application.use_cases.event_use_cases import EventUseCases


class UpdateEventRequest(BaseModel):
    action: Optional[ActionType] = None
    context: Optional[List[str]] = None
    court_zone: Optional[CourtZone] = None
    goal_zone: Optional[int] = Field(None, ge=1, le=9)
    defense_at_moment: Optional[DefenseType] = None
    rival_goalkeeper: Optional[int] = None
    turnover_type: Optional[str] = None
    recovery_type: Optional[str] = None

router = APIRouter(prefix="/events", tags=["Events"])

def get_event_use_cases():
    match_repo = MongoMatchRepository()
    event_repo = MongoEventRepository()
    return EventUseCases(event_repo, match_repo)

@router.post("/", response_model=Event)
async def register_event(
    event: Event, 
    use_cases: EventUseCases = Depends(get_event_use_cases)
):
    created_event = await use_cases.register_event(event)
    if not created_event:
        raise HTTPException(status_code=404, detail="Match not found")
    return created_event

@router.delete("/last/{match_id}", response_model=Match)
async def undo_last_event(
    match_id: str,
    use_cases: EventUseCases = Depends(get_event_use_cases)
):
    match = await use_cases.undo_last_event(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="No event to delete or match not found")
    return match

@router.get("/{match_id}", response_model=List[Event])
async def list_events(
    match_id: str,
    use_cases: EventUseCases = Depends(get_event_use_cases)
):
    return await use_cases.list_events_by_match(match_id)


@router.delete("/{event_id}", response_model=Event)
async def delete_event(
    event_id: str,
    use_cases: EventUseCases = Depends(get_event_use_cases)
):
    event = await use_cases.delete_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.patch("/{event_id}", response_model=Event)
async def update_event(
    event_id: str,
    body: UpdateEventRequest,
    use_cases: EventUseCases = Depends(get_event_use_cases)
):
    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    event = await use_cases.update_event(event_id, update_data)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
