from typing import Optional
from src.core.domain.event import Event
from src.core.domain.match import Match
from src.core.domain.enums import ActionType
from src.core.ports.event_repository import EventRepository
from src.core.ports.match_repository import MatchRepository

GOAL_ACTIONS = {ActionType.GOL, ActionType.GOL_7M, ActionType.GOL_CAMPO_A_CAMPO}

class EventUseCases:
    def __init__(
        self, 
        event_repository: EventRepository, 
        match_repository: MatchRepository
    ):
        self.event_repository = event_repository
        self.match_repository = match_repository

    async def register_event(self, event: Event) -> Optional[Event]:
        match = await self.match_repository.get_by_id(event.match_id)
        if not match:
            return None
        
        created_event = await self.event_repository.create(event)
        
        if event.action in GOAL_ACTIONS:
            update_data = {}
            if event.team == "A":
                update_data["local_score"] = match.local_score + 1
            else:
                update_data["visitor_score"] = match.visitor_score + 1
            await self.match_repository.update(event.match_id, update_data)
            
        return created_event

    async def undo_last_event(self, match_id: str) -> Optional[Match]:
        deleted_event = await self.event_repository.delete_last_by_match(match_id)
        if not deleted_event:
            return None

        match = await self.match_repository.get_by_id(match_id)
        if not match:
            return None

        if deleted_event.action in GOAL_ACTIONS:
            update_data = {}
            if deleted_event.team == "A":
                update_data["local_score"] = max(0, match.local_score - 1)
            else:
                update_data["visitor_score"] = max(0, match.visitor_score - 1)
            match = await self.match_repository.update(match_id, update_data)

        return match

    async def list_events_by_match(self, match_id: str) -> list[Event]:
        return await self.event_repository.list_by_match(match_id)

    async def delete_event(self, event_id: str) -> Optional[Event]:
        event = await self.event_repository.get_by_id(event_id)
        if not event:
            return None

        if event.action in GOAL_ACTIONS:
            match = await self.match_repository.get_by_id(event.match_id)
            if match:
                update_data = {}
                if event.team == "A":
                    update_data["local_score"] = max(0, match.local_score - 1)
                else:
                    update_data["visitor_score"] = max(0, match.visitor_score - 1)
                await self.match_repository.update(event.match_id, update_data)

        await self.event_repository.delete_by_id(event_id)
        return event

    async def update_event(self, event_id: str, update_data: dict) -> Optional[Event]:
        event = await self.event_repository.get_by_id(event_id)
        if not event:
            return None

        old_action = event.action
        new_action = update_data.get("action", old_action)

        old_is_goal = old_action in GOAL_ACTIONS
        new_is_goal = new_action in GOAL_ACTIONS

        if old_is_goal != new_is_goal:
            match = await self.match_repository.get_by_id(event.match_id)
            if match:
                score_update = {}
                if event.team == "A":
                    field = "local_score"
                    current = match.local_score
                else:
                    field = "visitor_score"
                    current = match.visitor_score

                if old_is_goal and not new_is_goal:
                    score_update[field] = max(0, current - 1)
                else:
                    score_update[field] = current + 1

                await self.match_repository.update(event.match_id, score_update)

        return await self.event_repository.update_by_id(event_id, update_data)
