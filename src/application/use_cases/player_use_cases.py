from typing import List, Optional
from src.core.domain.player import Player
from src.core.ports.player_repository import PlayerRepository

class PlayerUseCases:
    def __init__(self, player_repository: PlayerRepository):
        self.player_repository = player_repository

    async def add_player(self, player: Player) -> Player:
        return await self.player_repository.create(player)

    async def add_players_bulk(self, players: List[Player]) -> List[Player]:
        return await self.player_repository.create_many(players)

    async def list_players(self, match_id: str, team: Optional[str] = None) -> List[Player]:
        return await self.player_repository.list_by_match(match_id, team)

    async def delete_player(self, match_id: str, player_id: str) -> bool:
        return await self.player_repository.delete(match_id, player_id)
