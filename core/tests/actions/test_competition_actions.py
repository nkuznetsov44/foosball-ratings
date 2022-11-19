from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from pytz import UTC
import pytest
from hamcrest import assert_that, equal_to, has_properties, match_equality, not_none

from common.entities.enums import CompetitionType, RatingsStateStatus
from common.entities.match import GrandFinalOptions
from common.entities.ratings_state import RatingsState
from common.entities.player_state import PlayerState
from common.entities.competition import Competition
from common.interactions.core.requests.competition import (
    CreateCompetitionRequest,
    CompetitionTeam,
    CompetitionMatch,
    CompetitionMatchSet,
)
from core.actions.competition import CreateProcessedCompetitionAction
from core.actions.processing import ProcessCompetitionAction


class TestCreateProcessedCompetitionAction:
    @pytest.mark.asyncio
    async def test_creates_competition(
        self, storage, stored_tournament, stored_ratings_state, create_competition_request, expected_competition,
    ):
        result = await CreateProcessedCompetitionAction(request=create_competition_request).run()
        competition = await storage.competitions.get(result.last_competition_id)
        assert_that(competition, equal_to(
            replace(
                expected_competition,
                id=result.last_competition_id,
            )
        ))

    @pytest.mark.asyncio
    async def test_calls_ratings_calculation(
        self, storage, stored_tournament, stored_ratings_state, create_competition_request, expected_competition, mock_action
    ):
        mock = mock_action(ProcessCompetitionAction, None)
        await CreateProcessedCompetitionAction(request=create_competition_request).run()
        assert_that(
            mock.call_args.kwargs, equal_to(
                {
                    "competition": expected_competition,
                }
            )
        )

    @pytest.fixture
    def create_competition_request(self, stored_tournament, stored_player1, stored_player2):
        return CreateCompetitionRequest(
            tournament_id=stored_tournament.id,
            external_id=42,
            competition_type=CompetitionType.OS,
            order=1,
            evks_importance=Decimal("0.75"),
            cumulative_coefficient=Decimal("1.0"),
            start_datetime=datetime(
                year=2022, month=8, day=13, hour=3, minute=12, second=58, tzinfo=UTC
            ),
            end_datetime=datetime(
                year=2022, month=8, day=13, hour=6, minute=12, second=58, tzinfo=UTC
            ),
            matches=[
                CompetitionMatch(
                    external_id=42,
                    first_team_external_id=1,
                    second_team_external_id=2,
                    order=1,
                    sets=[
                        CompetitionMatchSet(
                            external_id=1,
                            order=1,
                            first_team_score=5,
                            second_team_score=2,
                        ),
                        CompetitionMatchSet(
                            external_id=2,
                            order=2,
                            first_team_score=5,
                            second_team_score=3,
                        )
                    ],
                    force_qualification=False,
                    is_forfeit=False,
                    grand_final_options=GrandFinalOptions(
                        sets_winner_bracket=2,
                        sets_looser_bracket=3,
                    ),
                    start_datetime=datetime(
                        year=2022, month=8, day=13, hour=3, minute=12, second=58, tzinfo=UTC
                    ),
                    end_datetime=datetime(
                        year=2022, month=8, day=13, hour=6, minute=12, second=58, tzinfo=UTC
                    ),
                ),
            ],
            teams=[
                CompetitionTeam(
                    external_id=1,
                    competition_place=1,
                    competition_order=1,
                    first_player_id=stored_player1.id,
                    second_player_id=None,
                ),
                CompetitionTeam(
                    external_id=2,
                    competition_place=2,
                    competition_order=2,
                    first_player_id=stored_player2.id,
                    second_player_id=None,
                )
            ],
        )

    @pytest.fixture
    def expected_competition(self, stored_tournament):
        return Competition(
            id=match_equality(not_none()),
            tournament=stored_tournament,
            competition_type=CompetitionType.OS,
            order=1,
            evks_importance_coefficient=Decimal("0.75"),
            cumulative_coefficient=Decimal("1.0"),
            start_datetime=datetime(
                year=2022, month=8, day=13, hour=3, minute=12, second=58, tzinfo=UTC,
            ),
            end_datetime=datetime(
                year=2022, month=8, day=13, hour=6, minute=12, second=58, tzinfo=UTC,
            ),
            external_id=42,
        )
