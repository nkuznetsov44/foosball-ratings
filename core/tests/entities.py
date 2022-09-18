from decimal import Decimal
from datetime import datetime

import pytest_asyncio

from common.entities.competition import Competition
from common.entities.enums import (
    City,
    CompetitionType,
    EvksPlayerRank,
    RatingType,
    RatingsStateStatus,
)
from common.entities.match import Match, MatchSet
from common.entities.player import Player
from common.entities.player_state import PlayerState
from common.entities.ratings_state import PlayerStateSet, RatingsState
from common.entities.team import Team
from common.entities.tournament import Tournament


@pytest_asyncio.fixture
async def player1(storage):
    return await storage.players.create(
        Player(id=1, first_name="Никита", last_name="Кузнецов", city=City.MOSCOW)
    )


@pytest_asyncio.fixture
async def player2(storage):
    return await storage.players.create(
        Player(id=2, first_name="Артем", last_name="Бочков", city=City.MOSCOW)
    )


@pytest_asyncio.fixture
async def player3(storage):
    return await storage.players.create(
        Player(id=3, first_name="Роман", last_name="Бушуев", city=City.MOSCOW)
    )


@pytest_asyncio.fixture
async def player4(storage):
    return await storage.players.create(
        Player(id=4, first_name="Анна", last_name="Мамаева", city=City.MOSCOW)
    )


@pytest_asyncio.fixture
async def player1_state(storage, player1):
    return await storage.player_states.create(
        PlayerState(
            id=1,
            previous_state_id=None,
            player=player1,
            matches_played=100,
            matches_won=50,
            last_match=None,
            ratings={RatingType.EVKS: 1710},
            evks_rank=EvksPlayerRank.SEMIPRO,
            is_evks_rating_active=True,
        )
    )


@pytest_asyncio.fixture
async def player2_state(storage, player2):
    return await storage.player_states.create(
        PlayerState(
            id=2,
            previous_state_id=None,
            player=player2,
            matches_played=100,
            matches_won=50,
            last_match=None,
            ratings={RatingType.EVKS: 2063},
            evks_rank=EvksPlayerRank.MASTER,
            is_evks_rating_active=True,
        )
    )


@pytest_asyncio.fixture
async def player3_state(storage, player3):
    return await storage.player_states.create(
        PlayerState(
            id=3,
            previous_state_id=None,
            player=player3,
            matches_played=100,
            matches_won=50,
            last_match=None,
            ratings={RatingType.EVKS: 1638},
            evks_rank=EvksPlayerRank.SEMIPRO,
            is_evks_rating_active=True,
        )
    )


@pytest_asyncio.fixture
async def player4_state(storage, player4):
    return await storage.player_states.create(
        PlayerState(
            id=4,
            previous_state_id=None,
            player=player4,
            matches_played=100,
            matches_won=50,
            last_match=None,
            ratings={RatingType.EVKS: 1218},
            evks_rank=EvksPlayerRank.NOVICE,
            is_evks_rating_active=True,
        )
    )


@pytest_asyncio.fixture
async def ratings_state(storage, player1_state, player2_state, player3_state, player4_state):
    return await storage.ratings_states.create(
        RatingsState(
            id=1,
            previous_state_id=None,
            player_states=PlayerStateSet([player1_state, player2_state, player3_state, player4_state]),
            last_competition=None,
            status=RatingsStateStatus.PUBLISHED,
        )
    )


@pytest_asyncio.fixture
async def tournament(storage):
    return await storage.tournaments.create(
        Tournament(
            id=1,
            name="Test tournament",
            city=City.MOSCOW,
            url=None,
        )
    )


@pytest_asyncio.fixture
async def doubles_competition(storage, tournament):
    return await storage.competitions.create(
        Competition(
            id=1,
            tournament=tournament,
            competition_type=CompetitionType.OD,
            evks_importance_coefficient=Decimal("0.75"),
            start_datetime=datetime(year=2022, month=8, day=13, hour=3, minute=12, second=58),
            end_datetime=datetime(year=2022, month=8, day=13, hour=4, minute=12, second=58),
        )
    )


@pytest_asyncio.fixture
async def singles_competition(storage, tournament):
    return await storage.competitions.create(
        Competition(
            id=2,
            tournament=tournament,
            competition_type=CompetitionType.OS,
            evks_importance_coefficient=Decimal("0.75"),
            start_datetime=datetime(year=2022, month=8, day=14, hour=3, minute=12, second=58),
            end_datetime=datetime(year=2022, month=8, day=14, hour=4, minute=12, second=58),
        )
    )


@pytest_asyncio.fixture
async def doubles_match_teams(storage, doubles_competition, player1, player2, player3, player4):
    first_team = await storage.teams.create(
        Team(
            id=1,
            competition=doubles_competition,
            first_player=player1,
            second_player=player2,
            competition_place=1,
        )
    )
    second_team = await storage.teams.create(
        Team(
            id=2,
            competition=doubles_competition,
            first_player=player3,
            second_player=player4,
            competition_place=2,
        )
    )
    return first_team, second_team


@pytest_asyncio.fixture
async def doubles_match(storage, doubles_competition, doubles_match_teams):
    first_team, second_team = doubles_match_teams
    return await storage.matches.create(
        Match(
            id=1,
            competition=doubles_competition,
            first_team=first_team,
            second_team=second_team,
            start_datetime=doubles_competition.start_datetime,
            end_datetime=doubles_competition.end_datetime,
        )
    )


@pytest_asyncio.fixture
async def doubles_match_sets(storage, doubles_match):
    return [
        await storage.sets.create(
            MatchSet(
                id=1, match=doubles_match, order=1, first_team_score=5, second_team_score=2
            ),
        ),
        await storage.sets.create(
            MatchSet(
                id=2, match=doubles_match, order=2, first_team_score=5, second_team_score=2
            ),
        ),
        await storage.sets.create(
            MatchSet(
                id=3, match=doubles_match, order=3, first_team_score=2, second_team_score=5
            ),
        ),
        await storage.sets.create(
            MatchSet(
                id=4, match=doubles_match, order=4, first_team_score=5, second_team_score=2
            ),
        ),
    ]


@pytest_asyncio.fixture
async def singles_match_teams(storage, singles_competition, player2, player4):
    first_team = await storage.teams.create(
        Team(
            id=3,
            competition=singles_competition,
            first_player=player2,
            second_player=None,
            competition_place=1,
        )
    )
    second_team = await storage.teams.create(
        Team(
            id=4,
            competition=singles_competition,
            first_player=player4,
            second_player=None,
            competition_place=2,
        )
    )
    return first_team, second_team


@pytest_asyncio.fixture
async def singles_match(storage, singles_competition, singles_match_teams):
    first_team, second_team = singles_match_teams
    return await storage.matches.create(
        Match(
            id=2,
            competition=singles_competition,
            first_team=first_team,
            second_team=second_team,
            start_datetime=singles_competition.start_datetime,
            end_datetime=singles_competition.end_datetime,
        )
    )


@pytest_asyncio.fixture
async def singles_match_sets(storage, singles_match):
    return [
        await storage.sets.create(
            MatchSet(
                id=5, match=singles_match, order=1, first_team_score=1, second_team_score=5
            ),
        ),
        await storage.sets.create(
            MatchSet(
                id=6, match=singles_match, order=2, first_team_score=2, second_team_score=5
            ),
        ),
        await storage.sets.create(
            MatchSet(
                id=7, match=singles_match, order=3, first_team_score=5, second_team_score=3
            ),
        ),
        await storage.sets.create(
            MatchSet(
                id=8, match=singles_match, order=4, first_team_score=4, second_team_score=5
            ),
        ),
    ]
