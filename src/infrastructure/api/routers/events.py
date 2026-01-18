from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.core.domain.event import Event
from src.infrastructure.persistence.repositories.mongo_match_repository import MongoMatchRepository
from src.infrastructure.persistence.repositories.mongo_event_repository import MongoEventRepository
from src.application.use_cases.event_use_cases import EventUseCases

router = APIRouter(prefix="/events", tags=["Events"])

# Dependency Injection Helper
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

@router.delete("/last/{match_id}")
async def undo_last_event(
    match_id: str,
    use_cases: EventUseCases = Depends(get_event_use_cases)
):
    success = await use_cases.undo_last_event(match_id)
    if not success:
        raise HTTPException(status_code=404, detail="No event to delete or match not found")
    return {"status": "deleted"}
