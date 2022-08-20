import pytest
from hamcrest import assert_that, equal_to
from decimal import Decimal
from common.enums import RatingType, CompetitionType, EvksPlayerRank, City
from core.processing.calculators.evks import EvksRatingCalculator
from core.entities.player import Player
from core.entities.match import Match, Team, MatchSet
from core.entities.competition import Competition
from core.entities.state import PlayerState, RatingsState


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
def ratings_state(player1, player2, player3, player4):
    return RatingsState(
        previous_state_id=None,
        player_states=[
            PlayerState(
                previous_state_id=None,
                player=player1,
                matches_played=100,
                matches_won=50,
                last_match=None,
                ratings={RatingType.EVKS: 1710},
                is_evks_rating_active=True,
            ),
            PlayerState(
                previous_state_id=None,
                player=player2,
                matches_played=100,
                matches_won=50,
                last_match=None,
                ratings={RatingType.EVKS: 2063},
                is_evks_rating_active=True,
            ),
            PlayerState(
                previous_state_id=None,
                player=player3,
                matches_played=100,
                matches_won=50,
                last_match=None,
                ratings={RatingType.EVKS: 1638},
                is_evks_rating_active=True,
            ),
            PlayerState(
                previous_state_id=None,
                player=player4,
                matches_played=100,
                matches_won=50,
                last_match=None,
                ratings={RatingType.EVKS: 1218},
                is_evks_rating_active=True,
            ),
        ],
        player_evks_ranks={
            1: EvksPlayerRank.SEMIPRO,
            2: EvksPlayerRank.MASTER,
            3: EvksPlayerRank.SEMIPRO,
            4: EvksPlayerRank.NOVICE,
        },
        last_competition=None,
    )


@pytest.fixture
def match1(player1, player2, player3, player4):
    return Match(
        first_team=Team(first_player=player1, second_player=player2),
        second_team=Team(first_player=player3, second_player=player4),
        sets=[
            MatchSet(order=1, first_team_score=5, second_team_score=2),
            MatchSet(order=2, first_team_score=5, second_team_score=2),
            MatchSet(order=3, first_team_score=2, second_team_score=5),
            MatchSet(order=4, first_team_score=5, second_team_score=2),
        ],
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def match2(player2, player4):
    return Match(
        first_team=Team(first_player=player2, second_player=None),
        second_team=Team(first_player=player4, second_player=None),
        sets=[
            MatchSet(order=1, first_team_score=1, second_team_score=5),
            MatchSet(order=2, first_team_score=2, second_team_score=5),
            MatchSet(order=3, first_team_score=5, second_team_score=3),
            MatchSet(order=4, first_team_score=4, second_team_score=5),
        ],
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def competition(match1, match2):
    return Competition(
        competition_type=CompetitionType.COD,
        evks_importance_coefficient=Decimal("0.75"),
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
        matches=[match1, match2],
    )


@pytest.fixture
def calculator(ratings_state):
    return EvksRatingCalculator(ratings_state)


def test_evks_calculation_doubles(
    calculator, competition, match1, player1, player2, player3, player4
):
    result = calculator.calculate(match=match1, competition=competition)
    # r = 2.547396728611409795104721012
    assert_that(result[player1], equal_to(1713))
    assert_that(result[player2], equal_to(2066))
    assert_that(result[player3], equal_to(1635))
    assert_that(result[player4], equal_to(1215))


def test_evks_calculation_singles(calculator, competition, match2, player2, player4):
    result = calculator.calculate(match=match2, competition=competition)
    # r = 35.72428301468905220089739857
    assert_that(result[player2], equal_to(2027))
    assert_that(result[player4], equal_to(1254))
