import pytest
import pytest_asyncio

from hamcrest import assert_that, equal_to, match_equality, not_none, has_item

from common.interactions.core.requests.player import CreatePlayersRequest, PlayerReq
from common.entities.enums import City
from core.actions.player import CreatePlayersAction


class TestPlayerHandler:
    @pytest.mark.asyncio
    async def test_response(self, core_client, player):
        response = await core_client.get(f"/api/v1/players/{player.id}")
        assert_that(response.status, equal_to(200))

        response_json = await response.json()
        assert_that(
            response_json,
            equal_to(
                {
                    "id": player.id,
                    "external_id": player.external_id,
                    "first_name": player.first_name,
                    "last_name": player.last_name,
                    "city": player.city.name,
                }
            ),
        )

    @pytest_asyncio.fixture
    async def player(self, stored_player1):
        return stored_player1


class TestPlayersHandler:
    @pytest.mark.asyncio
    async def test_response(self, core_client, request_data):
        response = await core_client.post("/api/v1/players", json=request_data)
        print(await response.json())
        assert_that(response.status, equal_to(200))

        response_json = await response.json()
        assert_that(
            response_json,
            has_item(
                {
                    "id": match_equality(not_none()),
                    "player": {
                        "id": match_equality(not_none()),
                        "external_id": 666,
                        "first_name": "John",
                        "last_name": "Doe",
                        "city": "MOSCOW",
                    },
                    "previous_state_id": None,
                    "last_match": None,
                    "matches_played": 0,
                    "matches_won": 0,
                    "ratings": {"EVKS": 1100, "CUMULATIVE": 0},
                    "is_evks_rating_active": False,
                    "evks_rank": "NOVICE",
                }
            ),
        )

    @pytest.mark.asyncio
    async def test_runs_action(
        self, mock_action, core_client, request_data, create_players_request
    ):
        mock = mock_action(CreatePlayersAction, None)
        await core_client.post("/api/v1/players", json=request_data)
        assert_that(
            mock.call_args.kwargs, equal_to({"request": create_players_request})
        )

    @pytest.fixture
    def request_data(self):
        return {
            "players": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "city": "MOSCOW",
                    "external_id": 666,
                },
            ]
        }

    @pytest.fixture
    def create_players_request(self):
        return CreatePlayersRequest(
            players=[
                PlayerReq(
                    first_name="John",
                    last_name="Doe",
                    city=City.MOSCOW,
                    external_id=666,
                    initial_evks_rating=None,
                    initial_cumulative_rating=None,
                    initial_matches_played=None,
                    initial_matches_won=None,
                    is_evks_rating_active=None,
                )
            ]
        )
