from fastapi import APIRouter, Depends
from fastapi.responses import Response
from src.infrastructure.persistence.repositories.mongo_event_repository import MongoEventRepository
from src.infrastructure.persistence.repositories.mongo_player_repository import MongoPlayerRepository
from src.application.use_cases.statistics_use_cases import StatisticsUseCases

router = APIRouter(prefix="/matches/{match_id}/statistics", tags=["Statistics"])

def get_stats_use_cases():
    return StatisticsUseCases(MongoEventRepository(), MongoPlayerRepository())

@router.get("/")
async def get_full_stats(
    match_id: str,
    use_cases: StatisticsUseCases = Depends(get_stats_use_cases)
):
    return await use_cases.calculate_full_statistics(match_id)

@router.get("/goalkeepers")
async def get_gk_stats(
    match_id: str,
    use_cases: StatisticsUseCases = Depends(get_stats_use_cases)
):
    return await use_cases.calculate_goalkeeper_statistics(match_id)

@router.get("/export/csv")
async def export_csv(
    match_id: str,
    use_cases: StatisticsUseCases = Depends(get_stats_use_cases)
):
    csv_content = await use_cases.generate_csv_export(match_id)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=match_{match_id}.csv"}
    )
