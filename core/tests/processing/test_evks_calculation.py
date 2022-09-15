from decimal import Decimal

import pytest
from hamcrest import assert_that, equal_to

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
from core.processing.calculators.evks import EvksRatingCalculator


@pytest.fixture
def player1():
    return Player(id=1, first_name="Никита", last_name="Кузнецов", city=City.MOSCOW)


@pytest.fixture
def player2():
    return Player(id=2, first_name="Артем", last_name="Бочков", city=City.MOSCOW)


@pytest.fixture
def player3():
    return Player(id=3, first_name="Роман", last_name="Бушуев", city=City.MOSCOW)


@pytest.fixture
def player4():
    return Player(id=4, first_name="Анна", last_name="Мамаева", city=City.MOSCOW)


@pytest.fixture
def player1_state(player1):
    return PlayerState(
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


@pytest.fixture
def player2_state(player2):
    return PlayerState(
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


@pytest.fixture
def player3_state(player3):
    return PlayerState(
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


@pytest.fixture
def player4_state(player4):
    return PlayerState(
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


@pytest.fixture
def player_states_set(player1_state, player2_state, player3_state, player4_state):
    return PlayerStateSet([player1_state, player2_state, player3_state, player4_state])


@pytest.fixture
def ratings_state(player_states_set):
    return RatingsState(
        id=1,
        previous_state_id=None,
        player_states=player_states_set,
        last_competition=None,
        status=RatingsStateStatus.PUBLISHED,
    )


@pytest.fixture
def tournament():
    return Tournament(
        id=1,
        name="Test tournament",
        city=City.MOSCOW,
        url=None,
    )


@pytest.fixture
def doubles_competition(tournament):
    return Competition(
        id=1,
        tournament=tournament,
        competition_type=CompetitionType.OD,
        evks_importance_coefficient=Decimal("0.75"),
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def singles_competition(tournament):
    return Competition(
        id=2,
        tournament=tournament,
        competition_type=CompetitionType.OS,
        evks_importance_coefficient=Decimal("0.75"),
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def doubles_match_teams(doubles_competition, player1, player2, player3, player4):
    first_team = Team(
        id=1,
        competition=doubles_competition,
        first_player=player1,
        second_player=player2,
        competition_place=1,
    )
    second_team = Team(
        id=2,
        competition=doubles_competition,
        first_player=player3,
        second_player=player4,
        competition_place=2,
    )
    return first_team, second_team


@pytest.fixture
def doubles_match(doubles_competition, doubles_match_teams):
    first_team, second_team = doubles_match_teams
    return Match(
        id=1,
        competition=doubles_competition,
        first_team=first_team,
        second_team=second_team,
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def doubles_match_sets(doubles_match):
    return [
        MatchSet(
            id=1, match=doubles_match, order=1, first_team_score=5, second_team_score=2
        ),
        MatchSet(
            id=2, match=doubles_match, order=2, first_team_score=5, second_team_score=2
        ),
        MatchSet(
            id=3, match=doubles_match, order=3, first_team_score=2, second_team_score=5
        ),
        MatchSet(
            id=4, match=doubles_match, order=4, first_team_score=5, second_team_score=2
        ),
    ]


@pytest.fixture
def singles_match_teams(singles_competition, player2, player4):
    first_team = Team(
        id=3,
        competition=singles_competition,
        first_player=player2,
        second_player=None,
        competition_place=1,
    )
    second_team = Team(
        id=4,
        competition=singles_competition,
        first_player=player4,
        second_player=None,
        competition_place=2,
    )
    return first_team, second_team


@pytest.fixture
def singles_match(singles_competition, singles_match_teams):
    first_team, second_team = singles_match_teams
    return Match(
        id=2,
        competition=singles_competition,
        first_team=first_team,
        second_team=second_team,
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def singles_match_sets(singles_match):
    return [
        MatchSet(
            id=5, match=singles_match, order=1, first_team_score=1, second_team_score=5
        ),
        MatchSet(
            id=6, match=singles_match, order=2, first_team_score=2, second_team_score=5
        ),
        MatchSet(
            id=7, match=singles_match, order=3, first_team_score=5, second_team_score=3
        ),
        MatchSet(
            id=8, match=singles_match, order=4, first_team_score=4, second_team_score=5
        ),
    ]


@pytest.fixture
def calculator(ratings_state):
    return EvksRatingCalculator(ratings_state)


def test_evks_calculation_doubles(
    calculator,
    doubles_competition,
    doubles_match,
    doubles_match_sets,
    player1,
    player2,
    player3,
    player4,
):
    result = calculator.calculate(
        competition=doubles_competition,
        match=doubles_match,
        match_sets=doubles_match_sets,
    )
    # r = 2.547396728611409795104721012
    assert_that(result[player1.id], equal_to(1713))
    assert_that(result[player2.id], equal_to(2066))
    assert_that(result[player3.id], equal_to(1635))
    assert_that(result[player4.id], equal_to(1215))


def test_evks_calculation_singles(
    calculator, singles_competition, singles_match, singles_match_sets, player2, player4
):
    result = calculator.calculate(
        competition=singles_competition,
        match=singles_match,
        match_sets=singles_match_sets,
    )
    # r = 35.72428301468905220089739857
    assert_that(result[player2.id], equal_to(2027))
    assert_that(result[player4.id], equal_to(1254))
