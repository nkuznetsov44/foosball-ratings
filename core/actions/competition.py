from common.entities.competition import Competition
from core.actions.abstract_action import AbstractAction


class GetPlayerCompetitionsAction(AbstractAction[list[Competition]]):
    def __init__(self, player_id: int) -> None:
        self.player_id = player_id

    async def handle(self) -> list[Competition]:
        return await self.storage.competitions.find_by_player(self.player_id)