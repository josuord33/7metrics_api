from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.core.domain.match import Match
from src.core.domain.enums import MatchStatus
from src.infrastructure.persistence.repositories.mongo_match_repository import MongoMatchRepository
from src.application.use_cases.match_use_cases import MatchUseCases

router = APIRouter(prefix="/matches", tags=["Matches"])

# Dependency Injection Helper
def get_match_use_cases():
    repo = MongoMatchRepository()
    return MatchUseCases(repo)

@router.post("/", response_model=Match)
async def create_match(
    match: Match, 
    use_cases: MatchUseCases = Depends(get_match_use_cases)
):
    return await use_cases.create_match(match)

@router.get("/", response_model=List[Match])
async def list_matches(
    skip: int = 0, 
    limit: int = 50, 
    use_cases: MatchUseCases = Depends(get_match_use_cases)
):
    return await use_cases.list_matches(skip, limit)

@router.get("/{match_id}", response_model=Match)
async def get_match(
    match_id: str, 
    use_cases: MatchUseCases = Depends(get_match_use_cases)
):
    match = await use_cases.get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.post("/{match_id}/start")
async def start_match(match_id: str, use_cases: MatchUseCases = Depends(get_match_use_cases)):
    match = await use_cases.get_match(match_id)
    if not match: raise HTTPException(404)
    # Use generic repository update
    repo = MongoMatchRepository() 
    return await repo.update(match_id, {"status": MatchStatus.IN_PROGRESS})

@router.post("/{match_id}/pause")
async def pause_match(match_id: str, use_cases: MatchUseCases = Depends(get_match_use_cases)):
    repo = MongoMatchRepository()
    return await repo.update(match_id, {"status": MatchStatus.PAUSED})

@router.post("/{match_id}/finish")
async def finish_match(match_id: str, use_cases: MatchUseCases = Depends(get_match_use_cases)):
    repo = MongoMatchRepository()
    return await repo.update(match_id, {"status": MatchStatus.FINISHED})
