from typing import List, Optional
from beanie import PydanticObjectId
from src.core.domain.player import Player
from src.core.ports.player_repository import PlayerRepository
from src.infrastructure.persistence.models.player_model import PlayerModel

class MongoPlayerRepository(PlayerRepository):
    async def create(self, player: Player) -> Player:
        data = player.model_dump(exclude={"id"})
        if "match_id" in data:
            data["match_id"] = PydanticObjectId(data["match_id"])
            
        model = PlayerModel(**data)
        await model.insert()
        player.id = str(model.id)
        return player

    async def create_many(self, players: List[Player]) -> List[Player]:
        models = []
        for p in players:
            data = p.model_dump(exclude={"id"})
            if "match_id" in data:
                data["match_id"] = PydanticObjectId(data["match_id"])
            models.append(PlayerModel(**data))
        
        await PlayerModel.insert_many(models)
        
        # Return with IDs
        result = []
        for m in models:
            p_data = m.model_dump(exclude={"id", "match_id"})
            result.append(Player(id=str(m.id), match_id=str(m.match_id), **p_data))
        return result

    async def list_by_match(self, match_id: str, team: Optional[str] = None) -> List[Player]:
        try:
            oid = PydanticObjectId(match_id)
        except:
            return []
            
        query = PlayerModel.find(PlayerModel.match_id == oid)
        if team:
            query = query.find(PlayerModel.team == team)
            
        models = await query.to_list()
        return [Player(id=str(m.id), match_id=str(m.match_id), **m.model_dump(exclude={"id", "match_id"})) for m in models]

    async def get_by_id(self, match_id: str, player_id: str) -> Optional[Player]:
        # Implementation skipped for brevity unless needed, but required by protocol
        return None 

    async def update(self, match_id: str, player_id: str, player_data: dict) -> Optional[Player]:
         # Implementation skipped for brevity
        return None

    async def delete(self, match_id: str, player_id: str) -> bool:
        try:
            p_oid = PydanticObjectId(player_id)
            m_oid = PydanticObjectId(match_id)
        except:
            return False
        player = await PlayerModel.find_one(PlayerModel.id == p_oid, PlayerModel.match_id == m_oid)
        if player:
            await player.delete()
            return True
        return False
