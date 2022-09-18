import pytest
import pytest_asyncio
from hamcrest import assert_that, equal_to, match_equality, not_none, has_item

from common.interactions.core.requests.player import CreatePlayersRequest, PlayerReq
from common.entities.enums import City, EvksPlayerRank, RatingType
from common.entities.player import Player
from common.entities.player_state import PlayerState
from core.actions.player import GetPlayerAction, CreatePlayersAction


class TestGetPlayerAction:
    @pytest.mark.asyncio
    async def test_get_player(self, player):
        result = await GetPlayerAction(player_id=player.id).run()
        assert_that(result, equal_to(player))

    @pytest_asyncio.fixture
    async def player(self, stored_player1):
        return stored_player1


class TestCreatePlayersAction:
    @pytest.mark.asyncio
    async def test_result(
        self, stored_ratings_state, create_players_request, expected_player_state
    ):
        result = await CreatePlayersAction(request=create_players_request).run()
        assert_that(result, equal_to([expected_player_state]))

    @pytest.mark.asyncio
    async def test_creates_player(
        self, stored_ratings_state, storage, create_players_request
    ):
        result = await CreatePlayersAction(request=create_players_request).run()
        player = await storage.players.get(result[0].player.id)
        assert_that(
            player,
            equal_to(
                Player(
                    id=match_equality(not_none()),
                    first_name="John",
                    last_name="Doe",
                    city=City.EKATERINBURG,
                    external_id=42,
                )
            ),
        )

    @pytest.mark.asyncio
    async def test_creates_ratings_state(
        self,
        stored_ratings_state,
        storage,
        create_players_request,
        expected_player_state,
    ):
        await CreatePlayersAction(request=create_players_request).run()
        new_state = await storage.ratings_states.get_actual()
        assert_that(new_state.player_states, has_item(expected_player_state))

    @pytest.fixture
    def create_players_request(self):
        return CreatePlayersRequest(
            players=[
                PlayerReq(
                    first_name="John",
                    last_name="Doe",
                    city=City.EKATERINBURG,
                    external_id=42,
                    initial_evks_rating=1666,
                    initial_cumulative_rating=0,
                    initial_matches_played=666,
                    initial_matches_won=66,
                    is_evks_rating_active=True,
                )
            ]
        )

    @pytest.fixture
    def expected_player_state(self):
        return PlayerState(
            id=match_equality(not_none()),
            previous_state_id=None,
            player=Player(
                id=match_equality(not_none()),
                first_name="John",
                last_name="Doe",
                city=City.EKATERINBURG,
                external_id=42,
            ),
            matches_played=666,
            matches_won=66,
            last_match=None,
            ratings={
                RatingType.EVKS: 1666,
                RatingType.CUMULATIVE: 0,
            },
            evks_rank=EvksPlayerRank.SEMIPRO,
            is_evks_rating_active=True,
        )
