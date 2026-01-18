from typing import Optional
from src.core.domain.event import Event
from src.core.domain.enums import ActionType
from src.core.ports.event_repository import EventRepository
from src.core.ports.match_repository import MatchRepository

class EventUseCases:
    def __init__(
        self, 
        event_repository: EventRepository, 
        match_repository: MatchRepository
    ):
        self.event_repository = event_repository
        self.match_repository = match_repository

    async def register_event(self, event: Event) -> Optional[Event]:
        # 1. Verify match exists
        match = await self.match_repository.get_by_id(event.match_id)
        if not match:
            return None
        
        # 2. Save event
        created_event = await self.event_repository.create(event)
        
        # 3. Update score if goal
        if event.action in [ActionType.GOL, ActionType.GOL_7M, ActionType.GOL_CAMPO_A_CAMPO]:
            update_data = {}
            if event.team == "A":
                update_data["local_score"] = match.local_score + 1
            else:
                update_data["visitor_score"] = match.visitor_score + 1
            await self.match_repository.update(event.match_id, update_data)
            
        return created_event

    async def undo_last_event(self, match_id: str) -> bool:
        # Simplification: Just deleting last event, would need to revert score logic here properly
        # Ideally fetch last event first, check if it was a goal, then revert score, then delete.
        return await self.event_repository.delete_last_by_match(match_id)
