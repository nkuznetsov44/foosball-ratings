from core.actions.abstract_action import AbstractAction, ActionContext
from core.actions.player import GetPlayerAction
from core.api.requests.tournament import CreateTournamentRequest, MatchReq
from core.entities.player import Player
from core.entities.match import Match, MatchSet, Team
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
        tournament_competitions: list[Competition] = []
        for competition_req in self._request.competitions:
            competition_matches: list[Match] = []
            for match_req in competition_req.matches:
                (
                    first_team,
                    second_team,
                ) = await self._construct_team_entities_for_match_req(match_req)
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
                    first_team=first_team,
                    second_team=second_team,
                    start_datetime=match_req.start_datetime,
                    end_datetime=match_req.end_datetime,
                    force_qualification=match_req.force_qualification,
                    sets=sets,
                )
                competition_matches.append(match)

            competition = Competition(
                external_id=competition_req.external_id,
                competition_type=competition_req.competition_type,
                evks_importance_coefficient=self._request.evks_importance_coefficient,
                start_datetime=competition_req.start_datetime,
                end_datetime=competition_req.end_datetime,
                matches=competition_matches,
            )
            tournament_competitions.append(competition)

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

    async def _construct_team_entities_for_match_req(
        self, match_req: MatchReq
    ) -> tuple[Team, Team]:
        team1_player1 = await self._get_player(match_req.first_team.first_player_id)
        if match_req.first_team.second_player_id:
            team1_player2 = await self._get_player(
                match_req.first_team.second_player_id
            )
        else:
            team1_player2 = None

        team2_player1 = await self._get_player(match_req.second_team.first_player_id)
        if match_req.second_team.second_player_id:
            team2_player2 = await self._get_player(
                match_req.second_team.second_player_id
            )
        else:
            team2_player2 = None

        team1 = Team(
            external_id=match_req.first_team.external_id,
            first_player=team1_player1,
            second_player=team1_player2,
        )
        team2 = Team(
            external_id=match_req.second_team.external_id,
            first_player=team2_player1,
            second_player=team2_player2,
        )
        return team1, team2

    async def _get_player(self, player_id: int) -> Player:
        return await GetPlayerAction(context=self._context, player_id=player_id).run()
