from core.actions.abstract_action import AbstractAction, ActionContext
from core.actions.player import GetPlayerAction
from core.api.requests.tournament import (
    CompetitionReq,
    CreateTournamentRequest,
    MatchReq,
    TeamReq,
)
from core.entities.player import Player
from core.entities.match import Match, MatchSet
from core.entities.team import Team
from core.entities.competition import Competition
from core.entities.tournament import Tournament


class CreateTournamentAction(AbstractAction):
    def __init__(
        self,
        *,
        context: ActionContext,
        request: CreateTournamentRequest,
    ) -> None:
        super().__init__(context)
        self._request = request

    async def run(self) -> Tournament:
        tournament_competitions = await self._construct_tournament_competitions(
            self._request.competitions
        )
        tournament = Tournament(
            external_id=self._request.external_id,
            name=self._request.name,
            city=self._request.city,
            url=self._request.url,
            competitions=tournament_competitions,
        )

        async with self._make_db_session()() as session:
            session.add(tournament)
            await session.commit()
            assert tournament.id is not None
            return tournament

    async def _construct_competition_teams(
        self, team_reqs: list[TeamReq]
    ) -> dict[int, Team]:
        """Returns a map of team_external_id -> Team"""
        teams_map: dict[int, Team] = {}
        for team_req in team_reqs:
            first_player = await self._get_player(team_req.first_player_id)
            second_player = None
            if team_req.second_player_id:
                second_player = await self._get_player(team_req.second_player_id)

            teams_map[team_req.external_id] = Team(
                external_id=team_req.external_id,
                first_player=first_player,
                second_player=second_player,
                competition_place=team_req.competition_place,
            )
        return teams_map

    async def _construct_competition_matches(
        self, match_reqs: list[MatchReq], competition_teams: dict[int, Team]
    ) -> list[Match]:
        competition_matches: list[Match] = []
        for match_req in match_reqs:
            sets = [
                MatchSet(
                    external_id=req.external_id,
                    order=req.order,
                    first_team_score=req.first_team_score,
                    second_team_score=req.second_team_score,
                )
                for req in match_req.sets
            ]
            match = Match(
                external_id=match_req.external_id,
                first_team=competition_teams[match_req.first_team_external_id],
                second_team=competition_teams[match_req.second_team_external_id],
                start_datetime=match_req.start_datetime,
                end_datetime=match_req.end_datetime,
                force_qualification=match_req.force_qualification,
                sets=sets,
            )
            competition_matches.append(match)
        return competition_matches

    async def _construct_tournament_competitions(
        self, competition_reqs: list[CompetitionReq]
    ) -> list[Competition]:
        tournament_competitions: list[Competition] = []
        for competition_req in competition_reqs:
            competition_teams = await self._construct_competition_teams(
                competition_req.teams
            )
            competition_matches = await self._construct_competition_matches(
                competition_req.matches, competition_teams
            )
            competition = Competition(
                external_id=competition_req.external_id,
                competition_type=competition_req.competition_type,
                evks_importance_coefficient=self._request.evks_importance_coefficient,
                start_datetime=competition_req.start_datetime,
                end_datetime=competition_req.end_datetime,
                matches=competition_matches,
            )
            tournament_competitions.append(competition)
        return tournament_competitions

    async def _get_player(self, player_id: int) -> Player:
        return await GetPlayerAction(context=self._context, player_id=player_id).run()
