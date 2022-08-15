import pytest
from core.api.schemas import CompetitionRequestSchema


@pytest.fixture
def competition_request():
    return {
        'matches': [
            {
                'first_player_id': 1,
                'first_player_id': 2,
                'start_time': '2014-12-22T03:12:58.019077+00:00',
                'end_time': '2014-12-22T03:12:58.019077+00:00',
                'sets': [
                    {
                        'first_player_score': 5,
                        'second_player_score': 3
                    },
                    {
                        'first_player_score': 5,
                        'second_player_score': 2
                    },
                    {
                        'first_player_score': 5,
                        'second_player_score': 1
                    }
                ]
            },
            {
                'first_player_id': 2,
                'first_player_id': 3,
                'start_time': '2014-12-22T03:12:58.019077+00:00',
                'end_time': '2014-12-22T03:12:58.019077+00:00',
                'sets': [
                    {
                        'first_player_score': 5,
                        'second_player_score': 3
                    },
                    {
                        'first_player_score': 0,
                        'second_player_score': 5
                    },
                    {
                        'first_player_score': 5,
                        'second_player_score': 1
                    }
                ]
            },
        ]
    }


def test_competition_request_schema(competition_request):
    CompetitionRequestSchema().load(competition_request)
