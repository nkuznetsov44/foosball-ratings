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
from common.entities.state import PlayerState, RatingsState
from common.entities.team import Team
from common.entities.tournament import Tournament
from core.processing.calculators.evks import EvksRatingCalculator


@pytest.fixture
def player1():
    player = Player(first_name="Никита", last_name="Кузнецов", city=City.MOSCOW)
    player.id = 1
    return player


@pytest.fixture
def player2():
    player = Player(first_name="Артем", last_name="Бочков", city=City.MOSCOW)
    player.id = 2
    return player


@pytest.fixture
def player3():
    player = Player(first_name="Роман", last_name="Бушуев", city=City.MOSCOW)
    player.id = 3
    return player


@pytest.fixture
def player4():
    player = Player(first_name="Анна", last_name="Мамаева", city=City.MOSCOW)
    player.id = 4
    return player


@pytest.fixture
def player_states(player1, player2, player3, player4):
    player_states = {}

    p1_state = PlayerState(
        previous_state_id=None,
        player=player1,
        matches_played=100,
        matches_won=50,
        last_match=None,
        ratings={RatingType.EVKS: 1710},
        is_evks_rating_active=True,
    )
    p1_state.id = 1
    p1_state.player_id = 1
    player_states[player1.id] = p1_state

    p2_state = PlayerState(
        previous_state_id=None,
        player=player2,
        matches_played=100,
        matches_won=50,
        last_match=None,
        ratings={RatingType.EVKS: 2063},
        is_evks_rating_active=True,
    )
    p2_state.id = 2
    p2_state.player_id = 2
    player_states[player2.id] = p2_state

    p3_state = PlayerState(
        previous_state_id=None,
        player=player3,
        matches_played=100,
        matches_won=50,
        last_match=None,
        ratings={RatingType.EVKS: 1638},
        is_evks_rating_active=True,
    )
    p3_state.id = 3
    p3_state.player_id = 3
    player_states[player3.id] = p3_state

    p4_state = PlayerState(
        previous_state_id=None,
        player=player4,
        matches_played=100,
        matches_won=50,
        last_match=None,
        ratings={RatingType.EVKS: 1218},
        is_evks_rating_active=True,
    )
    p4_state.id = 4
    p4_state.player_id = 4
    player_states[player4.id] = p4_state

    return player_states


@pytest.fixture
def ratings_state(player_states):
    return RatingsState(
        previous_state_id=None,
        player_states=player_states,
        evks_player_ranks={
            1: EvksPlayerRank.SEMIPRO,
            2: EvksPlayerRank.MASTER,
            3: EvksPlayerRank.SEMIPRO,
            4: EvksPlayerRank.NOVICE,
        },
        last_competition=None,
        status=RatingsStateStatus.PUBLISHED,
    )


@pytest.fixture
def tournament():
    return Tournament(
        name="Test tournament",
        city=City.MOSCOW,
        url=None,
    )


@pytest.fixture
def doubles_competition(tournament):
    return Competition(
        tournament=tournament,
        competition_type=CompetitionType.OD,
        evks_importance_coefficient=Decimal("0.75"),
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def singles_competition(tournament):
    return Competition(
        tournament=tournament,
        competition_type=CompetitionType.OS,
        evks_importance_coefficient=Decimal("0.75"),
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def doubles_match_teams(doubles_competition, player1, player2, player3, player4):
    first_team = Team(
        competition=doubles_competition,
        first_player=player1,
        second_player=player2,
        competition_place=1,
    )
    second_team = Team(
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
        competition=doubles_competition,
        first_team=first_team,
        second_team=second_team,
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def doubles_match_sets(doubles_match):
    return [
        MatchSet(match=doubles_match, order=1, first_team_score=5, second_team_score=2),
        MatchSet(match=doubles_match, order=2, first_team_score=5, second_team_score=2),
        MatchSet(match=doubles_match, order=3, first_team_score=2, second_team_score=5),
        MatchSet(match=doubles_match, order=4, first_team_score=5, second_team_score=2),
    ]


@pytest.fixture
def singles_match_teams(singles_competition, player2, player4):
    first_team = Team(
        competition=singles_competition,
        first_player=player2,
        second_player=None,
        competition_place=1,
    )
    second_team = Team(
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
        competition=singles_competition,
        first_team=first_team,
        second_team=second_team,
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def singles_match_sets(singles_match):
    return [
        MatchSet(match=singles_match, order=1, first_team_score=1, second_team_score=5),
        MatchSet(match=singles_match, order=2, first_team_score=2, second_team_score=5),
        MatchSet(match=singles_match, order=3, first_team_score=5, second_team_score=3),
        MatchSet(match=singles_match, order=4, first_team_score=4, second_team_score=5),
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
