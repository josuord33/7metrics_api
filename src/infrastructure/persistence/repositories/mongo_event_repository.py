from typing import List, Optional
from beanie import PydanticObjectId
from src.core.domain.event import Event
from src.core.ports.event_repository import EventRepository
from src.infrastructure.persistence.models.event_model import EventModel

class MongoEventRepository(EventRepository):
    async def create(self, event: Event) -> Event:
        event_dict = event.model_dump(exclude={"id"})
        # Convert match_id string to PydanticObjectId for reference
        if "match_id" in event_dict:
            event_dict["match_id"] = PydanticObjectId(event_dict["match_id"])
            
        model = EventModel(**event_dict)
        await model.insert()
        event.id = str(model.id)
        return event

    async def list_by_match(self, match_id: str) -> List[Event]:
        try:
            oid = PydanticObjectId(match_id)
        except:
            return []
        
        models = await EventModel.find(EventModel.match_id == oid).sort("-timestamp").to_list()
        # Convert back to domain entity
        events = []
        for m in models:
            data = m.model_dump(exclude={"id", "match_id"})
            events.append(Event(id=str(m.id), match_id=str(m.match_id), **data))
        return events

    async def delete_last_by_match(self, match_id: str) -> Optional[Event]:
        try:
            oid = PydanticObjectId(match_id)
        except:
            return None

        last_event = await EventModel.find(EventModel.match_id == oid).sort("-created_at").first_or_none()
        if not last_event:
            return None

        data = last_event.model_dump(exclude={"id", "match_id"})
        deleted_event = Event(id=str(last_event.id), match_id=str(last_event.match_id), **data)
        await last_event.delete()
        return deleted_event
