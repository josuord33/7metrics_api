import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.use_cases.event_use_cases import EventUseCases
from src.core.domain.event import Event
from src.core.domain.match import Match
from src.core.domain.enums import ActionType, TeamSide

@pytest.fixture
def mock_event_repo():
    return AsyncMock()

@pytest.fixture
def mock_match_repo():
    return AsyncMock()

@pytest.fixture
def event_use_cases(mock_event_repo, mock_match_repo):
    return EventUseCases(mock_event_repo, mock_match_repo)

@pytest.mark.asyncio
async def test_register_goal_updates_score(event_use_cases, mock_match_repo, mock_event_repo):
    # Arrange
    match_id = "match_123"
    initial_match = Match(
        id=match_id,
        team_a_name="Team A",
        team_b_name="Team B",
        local_score=10,
        visitor_score=10
    )
    
    event = Event(
        match_id=match_id,
        timestamp=120,
        time_formatted="02:00",
        player=7,
        team=TeamSide.A,
        action=ActionType.GOL
    )
    
    # Mock behavior
    mock_match_repo.get_by_id.return_value = initial_match
    # When create is called, return the event with an ID
    mock_event_repo.create.side_effect = lambda e: (setattr(e, 'id', 'event_1'), e)[1]

    # Act
    result = await event_use_cases.register_event(event)

    # Assert
    # 1. Verify event was created
    assert result is not None
    mock_event_repo.create.assert_called_once()
    
    # 2. Verify match score was updated
    # Check that update was called with correct match_id and incremented score
    mock_match_repo.update.assert_called_once()
    call_args = mock_match_repo.update.call_args
    assert call_args[0][0] == match_id
    assert call_args[0][1] == {"local_score": 11} # 10 + 1

@pytest.mark.asyncio
async def test_register_non_goal_does_not_update_score(event_use_cases, mock_match_repo, mock_event_repo):
    # Arrange
    match_id = "match_123"
    initial_match = Match(
        id=match_id,
        team_a_name="Team A",
        team_b_name="Team B",
        local_score=5
    )
    
    event = Event(
        match_id=match_id,
        timestamp=120,
        time_formatted="02:00",
        player=7,
        team=TeamSide.A,
        action=ActionType.PÉRDIDA # Not a goal
    )
    
    mock_match_repo.get_by_id.return_value = initial_match
    mock_event_repo.create.return_value = event

    # Act
    await event_use_cases.register_event(event)

    # Assert
    mock_event_repo.create.assert_called_once()
    mock_match_repo.update.assert_not_called() # Score should not change
