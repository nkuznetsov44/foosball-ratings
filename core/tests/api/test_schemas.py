import pytest
from core.api.schemas.tournament import CreateTournamentRequestSchema


@pytest.fixture
def create_tournament_request():
    return {
        "name": "Тестовый турнир",
        "city": "MOSCOW",
        "evks_importance_coefficient": "0.75",
        "url": "https://vk.invalid/tournament",
        "competitions": [
            {
                "competition_type": "OS",
                "start_datetime": "2022-12-22T03:12:58.019077+00:00",
                "end_datetime": "2022-12-22T03:12:58.019077+00:00",
                "matches": [
                    {
                        "first_team": {"first_player_id": 1, "second_player_id": None},
                        "second_team": {"first_player_id": 2, "second_player_id": None},
                        "sets": [
                            {"order": 1, "first_team_score": 5, "second_team_score": 2},
                            {"order": 2, "first_team_score": 5, "second_team_score": 1},
                            {"order": 3, "first_team_score": 5, "second_team_score": 0},
                        ],
                        "force_qualification": None,
                        "start_datetime": "2022-12-22T03:12:58.019077+00:00",
                        "end_datetime": "2022-12-22T03:12:58.019077+00:00",
                    }
                ],
            }
        ],
    }


def test_create_tournament_request_schema(create_tournament_request):
    CreateTournamentRequestSchema().load(create_tournament_request)


"""
Tournament(
    id=4,
    name='Тестовый турнир',
    city=<City.MOSCOW: 'Moscow'>,
    url='https://vk.invalid/tournament',
    competitions=[
        Competition(
            id=4,
            tournament_id=4,
            competition_type=<CompetitionType.OS: 'Open Singles'>,
            evks_importance_coefficient=Decimal('0.75'),
            start_datetime=datetime.datetime(
                2022, 12, 22, 3, 12, 58, 19077,
                tzinfo=datetime.timezone(datetime.timedelta(0), '+0000')
            ),
            end_datetime=datetime.datetime(
                2022, 12, 22, 3, 12, 58, 19077,
                tzinfo=datetime.timezone(datetime.timedelta(0), '+0000')
            ),
            matches=[
                Match(
                    id=4,
                    competition_id=4,
                    first_team=Team(
                        id=7,
                        first_player=Player(
                            id=1,
                            first_name='Никита',
                            last_name='Кузнецов',
                            city=<City.MOSCOW: 'Moscow'>
                        ),
                        second_player=None
                    ),
                    second_team=Team(
                        id=8,
                        first_player=Player(
                            id=2,
                            first_name='Артем',
                            last_name='Бочков',
                            city=<City.MOSCOW: 'Moscow'>
                        ),
                        second_player=None
                    ),
                    start_datetime=datetime.datetime(
                        2022, 12, 22, 3, 12, 58, 19077,
                        tzinfo=datetime.timezone(datetime.timedelta(0), '+0000')
                    ),
                    end_datetime=datetime.datetime(
                        2022, 12, 22, 3, 12, 58, 19077,
                        tzinfo=datetime.timezone(datetime.timedelta(0), '+0000')
                    ),
                    force_qualification=None,
                    sets=[
                        MatchSet(
                            id=10,
                            match_id=4,
                            order=1,
                            first_team_score=5,
                            second_team_score=2
                        ),
                        MatchSet(
                            id=11,
                            match_id=4,
                            order=2,
                            first_team_score=5,
                            second_team_score=1
                        ),
                        MatchSet(
                            id=12,
                            match_id=4,
                            order=3,
                            first_team_score=5,
                            second_team_score=0
                        )
                    ]
                )
            ]
        )
    ]
)
"""
