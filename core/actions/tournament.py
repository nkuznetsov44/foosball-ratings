from common.entities.competition import Competition
from common.entities.match import Match, MatchSet
from common.entities.player import Player
from common.entities.ratings_state import RatingsState
from common.entities.team import Team
from common.entities.tournament import Tournament
from core.actions.abstract_action import AbstractAction
from core.actions.processing import ProcessCompetitionAction
from common.interactions.core.requests.tournament import (
    CreateTournamentRequest,
    CompetitionReq,
    MatchReq,
    MatchSetReq,
    TeamReq,
)
from core.exceptions import PlayerStateNotFound


_TeamExternalId = int


# TODO: Refactor? Мне не нравится, что в Actions передается Request,
# который должен разбираться на уровне handler'a. Но тогда там нужно
# будет создавать все entities. Может, это и неплохо.


class CreateTournamentAction(AbstractAction[RatingsState]):
    def __init__(self, request: CreateTournamentRequest) -> None:
        self.request = request

    async def handle(self) -> RatingsState:
        ratings_state = await self.storage.ratings_states.get_actual()
        tournament = await self.storage.tournaments.create(
            Tournament(
                id=None,
                external_id=self.request.external_id,
                name=self.request.name,
                city=self.request.city,
                url=self.request.url,
            )
        )
        return await self._save_and_process_tournament_competitions(
            self.request.competitions, tournament, ratings_state
        )

    async def _save_and_process_tournament_competitions(
        self,
        competition_reqs: list[CompetitionReq],
        tournament: Tournament,
        ratings_state: RatingsState,
    ) -> RatingsState:
        for competition_req in competition_reqs:
            competition = await self.storage.competitions.create(
                Competition(
                    id=None,
                    tournament=tournament,
                    competition_type=competition_req.competition_type,
                    evks_importance_coefficient=self.request.evks_importance,
                    start_datetime=competition_req.start_datetime,
                    end_datetime=competition_req.end_datetime,
                    external_id=competition_req.external_id,
                )
            )
            competition_teams_map = await self._save_competition_teams(
                competition_req.teams,
                competition,
                ratings_state,
            )
            await self._save_competition_matches(
                competition_req.matches,
                competition,
                competition_teams_map,
            )
            return await self.run_subaction(ProcessCompetitionAction(competition))

    async def _save_competition_teams(
        self,
        team_reqs: list[TeamReq],
        competition: Competition,
        ratings_state: RatingsState,
    ) -> dict[_TeamExternalId, Team]:
        teams_map: dict[_TeamExternalId, Team] = {}
        for team_req in team_reqs:
            first_player = self._get_player(ratings_state, team_req.first_player_id)
            second_player = None
            if team_req.second_player_id:
                second_player = self._get_player(
                    ratings_state, team_req.second_player_id
                )

            teams_map[team_req.external_id] = await self.storage.teams.create(
                Team(
                    id=None,
                    competition=competition,
                    first_player=first_player,
                    second_player=second_player,
                    competition_place=team_req.competition_place,
                    external_id=team_req.external_id,
                )
            )
        return teams_map

    async def _save_competition_matches(
        self,
        match_reqs: list[MatchReq],
        competition: Competition,
        competition_teams_map: dict[int, Team],
    ) -> None:
        for match_req in match_reqs:
            match = await self.storage.matches.create(
                Match(
                    id=None,
                    competition=competition,
                    first_team=competition_teams_map[match_req.first_team_external_id],
                    second_team=competition_teams_map[
                        match_req.second_team_external_id
                    ],
                    start_datetime=match_req.start_datetime,
                    end_datetime=match_req.end_datetime,
                    force_qualification=match_req.force_qualification,
                    external_id=match_req.external_id,
                )
            )
            await self._save_match_sets(match_req.sets, match)

    async def _save_match_sets(self, set_reqs: list[MatchSetReq], match: Match) -> None:
        for set_req in set_reqs:
            await self.storage.sets.create(
                MatchSet(
                    id=None,
                    match=match,
                    order=set_req.order,
                    first_team_score=set_req.first_team_score,
                    second_team_score=set_req.second_team_score,
                    external_id=set_req.external_id,
                )
            )

    def _get_player(self, ratings_state: RatingsState, player_id: int) -> Player:
        player_state = ratings_state.player_states[player_id]
        if player_state is None:
            raise PlayerStateNotFound(player_id=player_id, current_state=ratings_state)
        return player_state.player
