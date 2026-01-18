from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from src.core.domain.player import Player
from src.infrastructure.persistence.repositories.mongo_player_repository import MongoPlayerRepository
from src.application.use_cases.player_use_cases import PlayerUseCases

router = APIRouter(prefix="/matches/{match_id}/players", tags=["Players"])

# Dependency Injection
def get_player_use_cases():
    return PlayerUseCases(MongoPlayerRepository())

class BulkPlayerCreate(BaseModel):
    players: List[dict] # Simplified for input

@router.post("/", response_model=Player)
async def create_player(
    match_id: str,
    player: Player,
    use_cases: PlayerUseCases = Depends(get_player_use_cases)
):
    # Ensure match_id in path matches body or override it
    player.match_id = match_id
    return await use_cases.add_player(player)

@router.post("/bulk", response_model=List[Player])
async def create_players_bulk(
    match_id: str,
    bulk_data: BulkPlayerCreate,
    use_cases: PlayerUseCases = Depends(get_player_use_cases)
):
    players_to_create = []
    for p_data in bulk_data.players:
        p_data["match_id"] = match_id
        players_to_create.append(Player(**p_data))
    
    return await use_cases.add_players_bulk(players_to_create)

@router.get("/", response_model=List[Player])
async def list_players(
    match_id: str,
    team: Optional[str] = None,
    use_cases: PlayerUseCases = Depends(get_player_use_cases)
):
    return await use_cases.list_players(match_id, team)

@router.delete("/{player_id}", status_code=204)
async def delete_player(
    match_id: str,
    player_id: str,
    use_cases: PlayerUseCases = Depends(get_player_use_cases)
):
    success = await use_cases.delete_player(match_id, player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Player not found")
