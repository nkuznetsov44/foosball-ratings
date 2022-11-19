from random import randint

import pytest
import pytest_asyncio

from hamcrest import assert_that, equal_to, match_equality, not_none, has_items, has_entries

from core.actions.competition import CreateProcessedCompetitionAction


class TestCompetitionHandler:
    @pytest.mark.asyncio
    async def test_response(
        self,
        stored_ratings_state,
        core_client,
        create_competition_request,
        expected_response,
    ):
        response = await core_client.post(
            "/api/v1/competitions", json=create_competition_request
        )
        response_json = await response.json()
        assert_that(response_json, has_entries(expected_response))

    @pytest.fixture
    def create_competition_request(
        self, player1, player2, team1_external_id, team2_external_id, stored_tournament,
    ):
        return {
            "tournament_id": stored_tournament.id,
            "competition_type": "OS",
            "evks_importance": "0.75",
            "cumulative_coefficient": "1.0",
            "order": 1,
            "start_datetime": "2022-12-22T03:12:58.019077+00:00",
            "end_datetime": "2022-12-22T03:12:58.019077+00:00",
            "teams": [
                {
                    "external_id": team1_external_id,
                    "first_player_id": player1.id,
                    "second_player_id": None,
                    "competition_place": 1,
                    "competition_order": 1,
                },
                {
                    "external_id": team2_external_id,
                    "first_player_id": player2.id,
                    "second_player_id": None,
                    "competition_place": 2,
                    "competition_order": 2,
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
                    "is_forfeit": False,
                    "start_datetime": "2022-12-22T03:12:58.019077+00:00",
                    "end_datetime": "2022-12-22T03:12:58.019077+00:00",
                    "order": 1,
                }
            ],
        }

    @pytest.fixture
    def expected_response(self, player1, player2):
        return {
            "id": match_equality(not_none()),
            "previous_state_id": match_equality(not_none()),
            "status": "READY_TO_PUBLISH",
            "last_competition_id": match_equality(not_none()),
            "player_states": has_items(
                has_entries({
                    "player": has_entries({
                        "first_name": "Никита",
                        "last_name": "Кузнецов",
                        "city": "MOSCOW",
                        "is_foreigner": False,
                        "external_id": None,
                        "id": player1.id,
                    }),
                    "matches_played": match_equality(not_none()),
                    "matches_won": match_equality(not_none()),
                    "last_match_id": match_equality(not_none()),
                    "ratings": has_entries({
                        "EVKS": match_equality(not_none()),
                        "CUMULATIVE": match_equality(not_none()),
                    }),
                    "evks_rank": match_equality(not_none()),
                    "is_evks_rating_active": match_equality(not_none()),
                    "id": match_equality(not_none()),
                    "previous_state_id": match_equality(not_none()),
                }),
                has_entries({
                    "player": has_entries({
                        "first_name": "Артем",
                        "last_name": "Бочков",
                        "city": "MOSCOW",
                        "is_foreigner": False,
                        "external_id": None,
                        "id": player2.id,
                    }),
                    "matches_played": match_equality(not_none()),
                    "matches_won": match_equality(not_none()),
                    "last_match_id": match_equality(not_none()),
                    "ratings": has_entries({
                        "EVKS": match_equality(not_none()),
                        "CUMULATIVE": match_equality(not_none()),
                    }),
                    "evks_rank": match_equality(not_none()),
                    "is_evks_rating_active": match_equality(not_none()),
                    "id": match_equality(not_none()),
                    "previous_state_id": match_equality(not_none()),
                }),
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
