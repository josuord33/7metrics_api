from typing import List, Optional
from beanie import PydanticObjectId
from src.core.domain.match import Match
from src.core.ports.match_repository import MatchRepository
from src.infrastructure.persistence.models.match_model import MatchModel

class MongoMatchRepository(MatchRepository):
    async def create(self, match: Match) -> Match:
        match_model = MatchModel(**match.model_dump(exclude={"id"}))
        await match_model.insert()
        match.id = str(match_model.id)
        return match

    async def get_by_id(self, match_id: str) -> Optional[Match]:
        try:
            oid = PydanticObjectId(match_id)
        except:
            return None
        model = await MatchModel.get(oid)
        if model:
            return Match(id=str(model.id), **model.model_dump(exclude={"id"}))
        return None

    async def list_all(self, skip: int = 0, limit: int = 50) -> List[Match]:
        models = await MatchModel.find_all().skip(skip).limit(limit).to_list()
        return [Match(id=str(m.id), **m.model_dump(exclude={"id"})) for m in models]

    async def update(self, match_id: str, match_data: dict) -> Optional[Match]:
        try:
            oid = PydanticObjectId(match_id)
        except:
            return None
        model = await MatchModel.get(oid)
        if not model:
            return None
        
        await model.update({"$set": match_data})
        updated_model = await MatchModel.get(oid)
        return Match(id=str(updated_model.id), **updated_model.model_dump(exclude={"id"}))

    async def delete(self, match_id: str) -> bool:
        try:
            oid = PydanticObjectId(match_id)
        except:
            return False
        model = await MatchModel.get(oid)
        if not model:
            return False
        await model.delete()
        return True
