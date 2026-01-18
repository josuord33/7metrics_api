import csv
import io
from typing import Dict, List
from src.core.ports.event_repository import EventRepository
from src.core.ports.player_repository import PlayerRepository
from src.core.domain.enums import ActionType, TeamSide

class StatisticsUseCases:
    def __init__(self, event_repository: EventRepository, player_repository: PlayerRepository):
        self.event_repository = event_repository
        self.player_repository = player_repository

    async def calculate_full_statistics(self, match_id: str) -> Dict:
        events = await self.event_repository.list_by_match(match_id)
        
        def calc_team_stats(team: str):
            team_events = [e for e in events if e.team == team]
            goals = len([e for e in team_events if e.action in [ActionType.GOL, ActionType.GOL_7M, ActionType.GOL_CAMPO_A_CAMPO]])
            shots = len([e for e in team_events if e.action in [
                ActionType.GOL, ActionType.GOL_7M, ActionType.GOL_CAMPO_A_CAMPO, 
                ActionType.PARADA, ActionType.FUERA, ActionType.POSTE, ActionType.FALLO_7M
            ]])
            saves = len([e for e in team_events if e.action == ActionType.PARADA])
            turnovers = len([e for e in team_events if e.action == ActionType.PERDIDA])
            
            return {
                "goals": goals,
                "shots": shots,
                "efficiency": round((goals / shots * 100) if shots > 0 else 0, 1),
                "saves": saves,
                "turnovers": turnovers,
                "possessions": len(team_events) # Simplification
            }

        return {
            "team_a": calc_team_stats(TeamSide.A),
            "team_b": calc_team_stats(TeamSide.B)
        }

    async def calculate_goalkeeper_statistics(self, match_id: str) -> Dict:
        events = await self.event_repository.list_by_match(match_id)
        # We need players to match numbers to names, but repo list_by_match protocol is simple.
        # Assuming we can fetch all players for match
        players = await self.player_repository.list_by_match(match_id)
        goalkeepers = [p for p in players if p.is_goalkeeper]
        
        gk_stats = []
        for gk in goalkeepers:
            rival_team = TeamSide.B if gk.team == TeamSide.A else TeamSide.A
            
            # Shots faced are events from RIVAL TEAM where rival_goalkeeper == gk.number
            shots_faced = [
                e for e in events 
                if e.team == rival_team 
                and e.rival_goalkeeper == gk.number
                and e.action in [ActionType.GOL, ActionType.GOL_7M, ActionType.PARADA, ActionType.FALLO_7M]
            ]
            
            saves = len([e for e in shots_faced if e.action in [ActionType.PARADA, ActionType.FALLO_7M]])
            total = len(shots_faced)
            
            gk_stats.append({
                "name": gk.name,
                "team": gk.team,
                "saves": saves,
                "total_shots": total,
                "percentage": round((saves / total * 100) if total > 0 else 0, 1)
            })
            
        return {"goalkeepers": gk_stats}

    async def generate_csv_export(self, match_id: str) -> str:
        events = await self.event_repository.list_by_match(match_id)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow(["Time", "Team", "Player", "Action", "Zone", "Result"])
        
        for event in events:
            writer.writerow([
                event.time_formatted,
                event.team,
                event.player,
                event.action,
                event.court_zone or "",
                "GOAL" if "GOL" in str(event.action) else "NO GOAL"
            ])
            
        return output.getvalue()
