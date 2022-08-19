import pytest
from core.api.schemas.competition import CreateCompetitionRequestSchema


@pytest.fixture
def competition_request():
    return {
        "tournament_id": 1,
        "competition_type": "OS",
        "city": "Москва",
        "evks_importance_coefficient": "0.75",
        "matches": [
            {
                "first_team": {"first_player_id": 1},
                "second_team": {"first_player_id": 2},
                "start_datetime": "2014-12-22T03:12:58.019077+00:00",
                "end_datetime": "2014-12-22T03:12:58.019077+00:00",
                "sets": [
                    {"first_team_score": 5, "second_team_score": 3},
                    {"first_team_score": 5, "second_team_score": 2},
                    {"first_team_score": 5, "second_team_score": 1},
                ],
            }
        ],
    }


def test_competition_request_schema(competition_request):
    CreateCompetitionRequestSchema().load(competition_request)
