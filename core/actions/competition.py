from common.entities.competition import Competition
from core.actions.abstract_action import AbstractAction


class GetPlayerCompetitionsAction(AbstractAction):
    def __init__(self, player_id: int) -> None:
        self.player_id = player_id

    async def handle(self) -> list[Competition]:
        return self.storage.competitions.find_by_player(self.player_id)
