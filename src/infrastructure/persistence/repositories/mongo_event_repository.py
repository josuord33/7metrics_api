from typing import List
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
            data = m.model_dump()
            data["match_id"] = str(data["match_id"]) # convert ObjectId back to str
            events.append(Event(id=str(m.id), **data))
        return events

    async def delete_last_by_match(self, match_id: str) -> bool:
        try:
            oid = PydanticObjectId(match_id)
        except:
            return False
            
        last_event = await EventModel.find(EventModel.match_id == oid).sort("-created_at").first_or_none()
        if last_event:
            await last_event.delete()
            return True
        return False
