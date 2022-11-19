from decimal import Decimal
from datetime import datetime

import pytest_asyncio

from common.entities.competition import Competition
from common.entities.enums import (
    CompetitionType,
    EvksPlayerRank,
    RatingType,
    RatingsStateStatus,
)
from common.entities.match import Match, MatchSet
from common.entities.player_state import PlayerState
from common.entities.ratings_state import PlayerStateSet, RatingsState
from common.entities.team import Team
from common.entities.enums import City
from common.entities.player import Player
from common.entities.tournament import Tournament


@pytest_asyncio.fixture
async def stored_player1(storage_context):
    async with storage_context() as storage:
        return await storage.players.create(
            Player(id=None, first_name="Никита", last_name="Кузнецов", city=City.MOSCOW)
        )


@pytest_asyncio.fixture
async def stored_player2(storage_context):
    async with storage_context() as storage:
        return await storage.players.create(
            Player(id=None, first_name="Артем", last_name="Бочков", city=City.MOSCOW)
        )


@pytest_asyncio.fixture
async def stored_player3(storage_context):
    async with storage_context() as storage:
        return await storage.players.create(
            Player(id=None, first_name="Роман", last_name="Бушуев", city=City.MOSCOW)
        )


@pytest_asyncio.fixture
async def stored_player4(storage_context):
    async with storage_context() as storage:
        return await storage.players.create(
            Player(id=None, first_name="Анна", last_name="Мамаева", city=City.MOSCOW)
        )


@pytest_asyncio.fixture
async def stored_tournament(storage_context):
    async with storage_context() as storage:
        return await storage.tournaments.create(
            Tournament(
                id=None,
                name="Test tournament",
                city=City.MOSCOW,
                url=None,
            )
        )


@pytest_asyncio.fixture
async def stored_player1_state(storage_context, stored_player1):
    async with storage_context() as storage:
        return await storage.player_states.create(
            PlayerState(
                id=None,
                previous_state_id=None,
                player=stored_player1,
                matches_played=100,
                matches_won=50,
                last_match_id=None,
                ratings={RatingType.EVKS: 1710},
                evks_rank=EvksPlayerRank.SEMIPRO,
                is_evks_rating_active=True,
            )
        )


@pytest_asyncio.fixture
async def stored_player2_state(storage_context, stored_player2):
    async with storage_context() as storage:
        return await storage.player_states.create(
            PlayerState(
                id=None,
                previous_state_id=None,
                player=stored_player2,
                matches_played=100,
                matches_won=50,
                last_match_id=None,
                ratings={RatingType.EVKS: 2063},
                evks_rank=EvksPlayerRank.MASTER,
                is_evks_rating_active=True,
            )
        )


@pytest_asyncio.fixture
async def stored_player3_state(storage_context, stored_player3):
    async with storage_context() as storage:
        return await storage.player_states.create(
            PlayerState(
                id=None,
                previous_state_id=None,
                player=stored_player3,
                matches_played=100,
                matches_won=50,
                last_match_id=None,
                ratings={RatingType.EVKS: 1638},
                evks_rank=EvksPlayerRank.SEMIPRO,
                is_evks_rating_active=True,
            )
        )


@pytest_asyncio.fixture
async def stored_player4_state(storage_context, stored_player4):
    async with storage_context() as storage:
        return await storage.player_states.create(
            PlayerState(
                id=None,
                previous_state_id=None,
                player=stored_player4,
                matches_played=100,
                matches_won=50,
                last_match_id=None,
                ratings={RatingType.EVKS: 1218},
                evks_rank=EvksPlayerRank.NOVICE,
                is_evks_rating_active=True,
            )
        )


@pytest_asyncio.fixture
async def stored_ratings_state(
    storage_context,
    stored_player1_state,
    stored_player2_state,
    stored_player3_state,
    stored_player4_state,
):
    async with storage_context() as storage:
        return await storage.ratings_states.create(
            RatingsState(
                id=None,
                previous_state_id=None,
                player_states=PlayerStateSet(
                    [
                        stored_player1_state,
                        stored_player2_state,
                        stored_player3_state,
                        stored_player4_state,
                    ]
                ),
                last_competition_id=None,
                status=RatingsStateStatus.PUBLISHED,
            )
        )


@pytest_asyncio.fixture
async def stored_doubles_competition(storage_context, stored_tournament):
    async with storage_context() as storage:
        return await storage.competitions.create(
            Competition(
                id=None,
                tournament=stored_tournament,
                order=1,
                competition_type=CompetitionType.OD,
                evks_importance_coefficient=Decimal("0.75"),
                cumulative_coefficient=Decimal("1.0"),
                start_datetime=datetime(
                    year=2022, month=8, day=13, hour=3, minute=12, second=58
                ),
                end_datetime=datetime(
                    year=2022, month=8, day=13, hour=4, minute=12, second=58
                ),
            )
        )


@pytest_asyncio.fixture
async def stored_singles_competition(storage_context, stored_tournament):
    async with storage_context() as storage:
        return await storage.competitions.create(
            Competition(
                id=None,
                tournament=stored_tournament,
                order=2,
                competition_type=CompetitionType.OS,
                evks_importance_coefficient=Decimal("0.75"),
                cumulative_coefficient=Decimal("1.0"),
                start_datetime=datetime(
                    year=2022, month=8, day=14, hour=3, minute=12, second=58
                ),
                end_datetime=datetime(
                    year=2022, month=8, day=14, hour=4, minute=12, second=58
                ),
            )
        )


@pytest_asyncio.fixture
async def stored_doubles_match_teams(
    storage_context,
    stored_doubles_competition,
    stored_player1,
    stored_player2,
    stored_player3,
    stored_player4,
):
    async with storage_context() as storage:
        first_team = await storage.teams.create(
            Team(
                id=None,
                competition_id=stored_doubles_competition.id,
                first_player=stored_player1,
                second_player=stored_player2,
                competition_place=1,
                competition_order=1,
            )
        )
        second_team = await storage.teams.create(
            Team(
                id=None,
                competition_id=stored_doubles_competition.id,
                first_player=stored_player3,
                second_player=stored_player4,
                competition_place=2,
                competition_order=2,
            )
        )
        return first_team, second_team


@pytest_asyncio.fixture
async def stored_doubles_match(
    storage_context, stored_doubles_competition, stored_doubles_match_teams
):
    async with storage_context() as storage:
        first_team, second_team = stored_doubles_match_teams
        return await storage.matches.create(
            Match(
                id=None,
                competition_id=stored_doubles_competition.id,
                order=1,
                first_team=first_team,
                second_team=second_team,
                start_datetime=stored_doubles_competition.start_datetime,
                end_datetime=stored_doubles_competition.end_datetime,
            )
        )


@pytest_asyncio.fixture
async def stored_doubles_match_sets(storage_context, stored_doubles_match):
    async with storage_context() as storage:
        return [
            await storage.sets.create(
                MatchSet(
                    id=None,
                    match_id=stored_doubles_match.id,
                    order=1,
                    first_team_score=5,
                    second_team_score=2,
                ),
            ),
            await storage.sets.create(
                MatchSet(
                    id=None,
                    match_id=stored_doubles_match.id,
                    order=2,
                    first_team_score=5,
                    second_team_score=2,
                ),
            ),
            await storage.sets.create(
                MatchSet(
                    id=None,
                    match_id=stored_doubles_match.id,
                    order=3,
                    first_team_score=2,
                    second_team_score=5,
                ),
            ),
            await storage.sets.create(
                MatchSet(
                    id=None,
                    match_id=stored_doubles_match.id,
                    order=4,
                    first_team_score=5,
                    second_team_score=2,
                ),
            ),
        ]


@pytest_asyncio.fixture
async def stored_singles_match_teams(
    storage_context, stored_singles_competition, stored_player2, stored_player4
):
    async with storage_context() as storage:
        first_team = await storage.teams.create(
            Team(
                id=None,
                competition_id=stored_singles_competition.id,
                first_player=stored_player2,
                second_player=None,
                competition_place=1,
                competition_order=1,
            )
        )
        second_team = await storage.teams.create(
            Team(
                id=None,
                competition_id=stored_singles_competition.id,
                first_player=stored_player4,
                second_player=None,
                competition_place=2,
                competition_order=2,
            )
        )
        return first_team, second_team


@pytest_asyncio.fixture
async def stored_singles_match(
    storage_context, stored_singles_competition, stored_singles_match_teams
):
    async with storage_context() as storage:
        first_team, second_team = stored_singles_match_teams
        return await storage.matches.create(
            Match(
                id=None,
                competition_id=stored_singles_competition.id,
                order=1,
                first_team=first_team,
                second_team=second_team,
                start_datetime=stored_singles_competition.start_datetime,
                end_datetime=stored_singles_competition.end_datetime,
            )
        )


@pytest_asyncio.fixture
async def stored_singles_match_sets(storage_context, stored_singles_match):
    async with storage_context() as storage:
        return [
            await storage.sets.create(
                MatchSet(
                    id=None,
                    match_id=stored_singles_match.id,
                    order=1,
                    first_team_score=1,
                    second_team_score=5,
                ),
            ),
            await storage.sets.create(
                MatchSet(
                    id=None,
                    match_id=stored_singles_match.id,
                    order=2,
                    first_team_score=2,
                    second_team_score=5,
                ),
            ),
            await storage.sets.create(
                MatchSet(
                    id=None,
                    match_id=stored_singles_match.id,
                    order=3,
                    first_team_score=5,
                    second_team_score=3,
                ),
            ),
            await storage.sets.create(
                MatchSet(
                    id=None,
                    match_id=stored_singles_match.id,
                    order=4,
                    first_team_score=4,
                    second_team_score=5,
                ),
            ),
        ]
