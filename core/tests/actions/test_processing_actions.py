import pytest
from hamcrest import assert_that, equal_to

from core.actions.processing import ProcessCompetitionAction


class TestProcessCompetitionAction:
    @pytest.mark.asyncio
    async def test_updates_ratings_state(
        self, storage, stored_ratings_state, stored_singles_competition
    ):
        result = await ProcessCompetitionAction(
            competition=stored_singles_competition
        ).run()
        ratings_state = await storage.ratings_states.get_actual()
        assert_that(ratings_state.id, equal_to(result.id))
        assert_that(ratings_state.previous_state_id, equal_to(stored_ratings_state.id))
