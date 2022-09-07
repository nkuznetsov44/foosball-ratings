from common.entities.match import Match
from core.actions.abstract_action import AbstractAction


class GetPlayerCompetitionMatchesAction(AbstractAction[list[Match]]):
    def __init__(self, player_id: int, competition_id: int) -> None:
        self.player_id = player_id
        self.competition_id = competition_id

    async def handle(self) -> list[Match]:
        return await self.storage.matches.find_by_player_and_competition(
            player_id=self.player_id,
            competition_id=self.competition_id,
        )
