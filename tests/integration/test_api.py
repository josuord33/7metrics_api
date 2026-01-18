import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_list_matches(client: AsyncClient):
    # 1. Create Match
    match_data = {
        "team_a_name": "Barcelona",
        "team_b_name": "Kiel",
        "defense_a": "6:0",
        "defense_b": "5:1"
    }
    response = await client.post("/matches/", json=match_data)
    assert response.status_code == 200
    created_match = response.json()
    assert created_match["team_a_name"] == "Barcelona"
    assert "id" in created_match
    match_id = created_match["id"]

    # 2. List Matches
    response = await client.get("/matches/")
    assert response.status_code == 200
    matches = response.json()
    assert len(matches) > 0
    assert matches[0]["id"] == match_id

@pytest.mark.asyncio
async def test_full_game_flow(client: AsyncClient):
    # 1. Start a Match
    match_res = await client.post("/matches/", json={
        "team_a_name": "Spain",
        "team_b_name": "France"
    })
    match_id = match_res.json()["id"]

    # 2. Record a Goal for Team A
    event_data = {
        "match_id": match_id,
        "timestamp": 45,
        "time_formatted": "00:45",
        "player": 10,
        "team": "A",
        "action": "GOL"
    }
    event_res = await client.post("/events/", json=event_data)
    assert event_res.status_code == 200
    
    # 3. Verify Match Score Updated
    match_check = await client.get(f"/matches/{match_id}")
    assert match_check.json()["local_score"] == 1
    assert match_check.json()["visitor_score"] == 0

    # 4. Record a Goal for Team B
    await client.post("/events/", json={
        "match_id": match_id,
        "timestamp": 90,
        "time_formatted": "01:30",
        "player": 5,
        "team": "B",
        "action": "GOL"
    })

    # 5. Verify Score is 1-1
    match_check_2 = await client.get(f"/matches/{match_id}")
    assert match_check_2.json()["local_score"] == 1
    assert match_check_2.json()["visitor_score"] == 1
