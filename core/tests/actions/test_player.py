import pytest

from hamcrest import assert_that, equal_to, match_equality, not_none

from common.interactions.core.requests.player import CreatePlayersRequest, PlayerReq
from common.entities.enums import City, EvksPlayerRank, RatingType
from common.entities.player import Player
from common.entities.player_state import PlayerState
from core.actions.player import GetPlayerAction, CreatePlayersAction


@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_player(player1):
    result = await GetPlayerAction(player_id=player1.id).run()
    assert_that(result, equal_to(player1))


@pytest.mark.skip
@pytest.mark.asyncio
async def test_create_players(storage):
    request = CreatePlayersRequest(
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

    result = await CreatePlayersAction(request=request).run()

    assert_that(
        result,
        equal_to(
            [
                PlayerState(
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
            ]
        ),
    )
