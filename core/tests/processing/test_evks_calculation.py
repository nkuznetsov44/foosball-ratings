import pytest
from hamcrest import assert_that, equal_to
from decimal import Decimal
from common.enums import RatingType, CompetitionType, EvksPlayerRank
from core.processing.calculators.evks import EvksRatingCalculator
from core.entities.player import Player
from core.entities.match import Match, Team, MatchSet
from core.entities.competition import Competition
from core.entities.state import PlayerState, RatingsState


@pytest.fixture
def player1():
    return Player(id=1, first_name="Никита", last_name="Кузнецов")


@pytest.fixture
def player2():
    return Player(id=2, first_name="Артем", last_name="Бочков")


@pytest.fixture
def player3():
    return Player(id=3, first_name="Роман", last_name="Бушуев")


@pytest.fixture
def player4():
    return Player(id=4, first_name="Анна", last_name="Мамаева")


@pytest.fixture
def ratings_state(player1, player2, player3, player4):
    return RatingsState(
        id=1,
        previous_state_id=1,
        player_states=[
            PlayerState(
                id=1,
                player=player1,
                matches_played=100,
                last_match=None,
                ratings={RatingType.EVKS: 1710},
                is_evks_rating_active=True,
            ),
            PlayerState(
                id=2,
                player=player2,
                matches_played=100,
                last_match=None,
                ratings={RatingType.EVKS: 2063},
                is_evks_rating_active=True,
            ),
            PlayerState(
                id=3,
                player=player3,
                matches_played=100,
                last_match=None,
                ratings={RatingType.EVKS: 1638},
                is_evks_rating_active=True,
            ),
            PlayerState(
                id=4,
                player=player4,
                matches_played=100,
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
        id=1,
        first_team=Team(id=1, first_player=player1, second_player=player2),
        second_team=Team(id=2, first_player=player3, second_player=player4),
        sets=[
            MatchSet(id=1, first_team_score=5, second_team_score=2),
            MatchSet(id=2, first_team_score=5, second_team_score=2),
            MatchSet(id=3, first_team_score=2, second_team_score=5),
            MatchSet(id=4, first_team_score=5, second_team_score=2),
        ],
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def match2(player2, player4):
    return Match(
        id=2,
        first_team=Team(id=3, first_player=player2, second_player=None),
        second_team=Team(id=4, first_player=player4, second_player=None),
        sets=[
            MatchSet(id=5, first_team_score=1, second_team_score=5),
            MatchSet(id=6, first_team_score=2, second_team_score=5),
            MatchSet(id=7, first_team_score=5, second_team_score=3),
            MatchSet(id=8, first_team_score=4, second_team_score=5),
        ],
        start_datetime="2022-08-13T03:12:58.019077+00:00",
        end_datetime="2022-08-13T03:12:58.019077+00:00",
    )


@pytest.fixture
def competition(match1, match2):
    return Competition(
        id=1,
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
