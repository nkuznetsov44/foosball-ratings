import pytest
from hamcrest import assert_that, equal_to, match_equality, not_none

from common.entities.enums import City
from common.entities.tournament import Tournament
from common.interactions.core.requests.tournament import CreateTournamentRequest
from core.actions.tournament import CreateTournamentAction


class TestCreateTournamentAction:
    @pytest.mark.asyncio
    async def test_result(self, create_tournament_request, expected_tournament, storage):
        result = await CreateTournamentAction(request=create_tournament_request).run()
        assert_that(result, equal_to(expected_tournament))

    @pytest.mark.asyncio
    async def test_creates_tournament(self, create_tournament_request, expected_tournament, storage):
        result = await CreateTournamentAction(request=create_tournament_request).run()
        tournament = await storage.tournaments.get(result.id)
        assert_that(tournament, equal_to(expected_tournament))

    @pytest.fixture
    def create_tournament_request(self):
        return CreateTournamentRequest(
            external_id=42,
            city=City.KAZAN,
            name="Test tournament name",
            url="https://tournament.invalid",
        )

    @pytest.fixture
    def expected_tournament(self):
        return Tournament(
            id=match_equality(not_none()),
            external_id=42,
            name="Test tournament name",
            url="https://tournament.invalid",
            city=City.KAZAN,
        )
