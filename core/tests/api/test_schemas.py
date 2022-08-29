import pytest

from core.api.schemas.tournament import CreateTournamentRequestSchema


@pytest.fixture
def create_tournament_request():
    return {
        "external_id": 1,
        "name": "Тестовый турнир",
        "city": "MOSCOW",
        "evks_importance_coefficient": "0.75",
        "url": "https://vk.invalid/tournament",
        "competitions": [
            {
                "external_id": 1,
                "competition_type": "OS",
                "start_datetime": "2022-12-22T03:12:58.019077+00:00",
                "end_datetime": "2022-12-22T03:12:58.019077+00:00",
                "teams": [
                    {
                        "external_id": 1,
                        "first_player_id": 1,
                        "second_player_id": None,
                        "competition_place": 1,
                    },
                    {
                        "external_id": 2,
                        "first_player_id": 2,
                        "second_player_id": None,
                        "competition_place": 2,
                    },
                ],
                "matches": [
                    {
                        "external_id": 1,
                        "first_team_external_id": 1,
                        "second_team_external_id": 2,
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
