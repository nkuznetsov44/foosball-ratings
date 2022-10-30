from sqlalchemy.exc import IntegrityError, NoResultFound

from common.entities.competition import Competition
from common.entities.match import Match, MatchSet
from common.entities.player import Player
from common.entities.ratings_state import RatingsState
from common.entities.team import Team
from common.interactions.core.requests.competition import (
    CreateCompetitionRequest,
    CompetitionTeam,
    CompetitionMatch,
    CompetitionMatchSet,
)

from core.actions.abstract_action import AbstractAction
from core.actions.processing import ProcessCompetitionAction
from core.exceptions import (
    PlayerStateNotFound,
    DuplicateTournamentCompetition,
    TournamentNotFound,
)


_TeamExternalId = int


class GetPlayerCompetitionsAction(AbstractAction[list[Competition]]):
    def __init__(self, player_id: int) -> None:
        self.player_id = player_id

    async def handle(self) -> list[Competition]:
        return await self.storage.competitions.find_by_player(self.player_id)


class CreateProcessedCompetitionAction(AbstractAction[RatingsState]):
    def __init__(self, request: CreateCompetitionRequest) -> None:
        self.request = request

    async def handle(self) -> RatingsState:
        # TODO: Catch sqlalchemy errors in storage and raise core exceptions there
        try:
            tournament = await self.storage.tournaments.get(self.request.tournament_id)
        except NoResultFound:
            raise TournamentNotFound(tournament_id=self.request.tournament_id)

        try:
            competition = await self.storage.competitions.create(
                Competition(
                    id=None,
                    tournament=tournament,
                    competition_type=self.request.competition_type,
                    evks_importance_coefficient=self.request.evks_importance,
                    start_datetime=self.request.start_datetime,
                    end_datetime=self.request.end_datetime,
                    external_id=self.request.external_id,
                )
            )
        except IntegrityError:
            raise DuplicateTournamentCompetition(
                tournament_id=self.request.tournament_id,
                competition_external_id=self.request.external_id,
            )

        competition_teams_map = await self._save_competition_teams(
            self.request.teams,
            competition,
        )
        await self._save_competition_matches(
            self.request.matches,
            competition,
            competition_teams_map,
        )
        return await self.run_subaction(ProcessCompetitionAction(competition))

    async def _save_competition_teams(
        self,
        competition_teams: list[CompetitionTeam],
        competition: Competition,
    ) -> dict[_TeamExternalId, Team]:
        ratings_state = await self.storage.ratings_states.get_actual()
        teams_map: dict[_TeamExternalId, Team] = {}
        for team in competition_teams:
            first_player = self._get_player(ratings_state, team.first_player_id)
            second_player = None
            if team.second_player_id:
                second_player = self._get_player(ratings_state, team.second_player_id)

            teams_map[team.external_id] = await self.storage.teams.create(
                Team(
                    id=None,
                    competition=competition,
                    first_player=first_player,
                    second_player=second_player,
                    competition_place=team.competition_place,
                    external_id=team.external_id,
                )
            )
        return teams_map

    async def _save_competition_matches(
        self,
        competition_matches: list[CompetitionMatch],
        competition: Competition,
        competition_teams_map: dict[_TeamExternalId, Team],
    ) -> None:
        for match in competition_matches:
            stored_match: Match = await self.storage.matches.create(
                Match(
                    id=None,
                    competition=competition,
                    first_team=competition_teams_map[match.first_team_external_id],
                    second_team=competition_teams_map[match.second_team_external_id],
                    start_datetime=match.start_datetime,
                    end_datetime=match.end_datetime,
                    force_qualification=match.force_qualification,
                    external_id=match.external_id,
                )
            )
            await self._save_match_sets(match.sets, stored_match)

    async def _save_match_sets(
        self, match_sets: list[CompetitionMatchSet], match: Match
    ) -> None:
        for mset in match_sets:
            await self.storage.sets.create(
                MatchSet(
                    id=None,
                    match=match,
                    order=mset.order,
                    first_team_score=mset.first_team_score,
                    second_team_score=mset.second_team_score,
                    external_id=mset.external_id,
                )
            )

    def _get_player(self, ratings_state: RatingsState, player_id: int) -> Player:
        player_state = ratings_state.player_states[player_id]
        if player_state is None:
            raise PlayerStateNotFound(player_id=player_id, current_state=ratings_state)
        return player_state.player
