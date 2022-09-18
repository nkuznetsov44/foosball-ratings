from random import randint

import pytest
import pytest_asyncio

from hamcrest import assert_that, equal_to, match_equality, not_none, has_items


class TestTournamentHandler:
    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_response(
        self,
        stored_ratings_state,
        core_client,
        create_tournament_request,
        expected_response,
    ):
        response = await core_client.post(
            "/api/v1/tournaments", json=create_tournament_request
        )
        assert_that(response.status, equal_to(200))

        response_json = await response.json()
        assert_that(response_json, equal_to(expected_response))

    @pytest.fixture
    def create_tournament_request(
        self, player1, player2, team1_external_id, team2_external_id
    ):
        return {
            "name": "Тестовый турнир",
            "city": "MOSCOW",
            "evks_importance": "0.75",
            "url": "https://vk.invalid/tournament",
            "competitions": [
                {
                    "competition_type": "OS",
                    "start_datetime": "2022-12-22T03:12:58.019077+00:00",
                    "end_datetime": "2022-12-22T03:12:58.019077+00:00",
                    "teams": [
                        {
                            "external_id": team1_external_id,
                            "first_player_id": player1.id,
                            "second_player_id": None,
                            "competition_place": 1,
                        },
                        {
                            "external_id": team2_external_id,
                            "first_player_id": player2.id,
                            "second_player_id": None,
                            "competition_place": 2,
                        },
                    ],
                    "matches": [
                        {
                            "first_team_external_id": team1_external_id,
                            "second_team_external_id": team2_external_id,
                            "sets": [
                                {
                                    "order": 1,
                                    "first_team_score": 5,
                                    "second_team_score": 2,
                                },
                                {
                                    "order": 2,
                                    "first_team_score": 5,
                                    "second_team_score": 1,
                                },
                                {
                                    "order": 3,
                                    "first_team_score": 5,
                                    "second_team_score": 0,
                                },
                            ],
                            "force_qualification": None,
                            "start_datetime": "2022-12-22T03:12:58.019077+00:00",
                            "end_datetime": "2022-12-22T03:12:58.019077+00:00",
                        }
                    ],
                }
            ],
        }

    @pytest.fixture
    def expected_response(self, player1, player2):
        return {
            "id": match_equality(not_none()),
            "status": "READY_TO_PUBLISH",
            "last_competition": {
                "id": match_equality(not_none()),
                "external_id": None,
                "tournament": {
                    "name": "Тестовый турнир",
                    "url": "https://vk.invalid/tournament",
                    "city": "MOSCOW",
                    "external_id": None,
                    "id": match_equality(not_none()),
                },
                "competition_type": "OS",
            },
            "player_states": has_items(
                [
                    {
                        "player": {
                            "first_name": "Никита",
                            "last_name": "Кузнецов",
                            "city": "MOSCOW",
                            "external_id": None,
                            "id": player1.id,
                        },
                        "matches_played": 1,
                        "matches_won": 1,
                        "ratings": {"EVKS": 1127, "CUMULATIVE": 0},
                        "evks_rank": "NOVICE",
                        "is_evks_rating_active": False,
                    },
                    {
                        "player": {
                            "first_name": "Артем",
                            "last_name": "Бочков",
                            "city": "MOSCOW",
                            "external_id": None,
                            "id": player2.id,
                        },
                        "matches_played": 1,
                        "matches_won": 0,
                        "ratings": {"EVKS": 1073, "CUMULATIVE": 0},
                        "evks_rank": "NOVICE",
                        "is_evks_rating_active": False,
                    },
                ]
            ),
        }

    @pytest_asyncio.fixture
    async def player1(self, stored_player1):
        return stored_player1

    @pytest_asyncio.fixture
    async def player2(self, stored_player2):
        return stored_player2

    @pytest.fixture
    def team1_external_id(self):
        return randint(10000, 100000)

    @pytest.fixture
    def team2_external_id(self):
        return randint(10000, 100000)
