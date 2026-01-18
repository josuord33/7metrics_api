from typing import List, Optional
from src.core.domain.match import Match
from src.core.ports.match_repository import MatchRepository

class MatchUseCases:
    def __init__(self, match_repository: MatchRepository):
        self.match_repository = match_repository

    async def create_match(self, match_data: Match) -> Match:
        return await self.match_repository.create(match_data)

    async def get_match(self, match_id: str) -> Optional[Match]:
        return await self.match_repository.get_by_id(match_id)

    async def list_matches(self, skip: int = 0, limit: int = 50) -> List[Match]:
        return await self.match_repository.list_all(skip, limit)
