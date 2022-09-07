from dataclasses import replace

from common.entities.player import Player
from common.entities.player_state import PlayerState
from core.actions.abstract_action import AbstractAction
from core.actions.player_state import CreateInitialPlayerStateAction
from core.actions.ratings_state import CreateRatingsStateAction
from common.interactions.core.requests.player import CreatePlayersRequest


_PlayerId = int


class GetPlayerAction(AbstractAction[Player]):
    def __init__(self, player_id: int) -> None:
        self.player_id = player_id

    async def handle(self) -> Player:
        return await self.storage.players.get(self.player_id)


class GetPlayersAction(AbstractAction[list[Player]]):
    async def handle(self) -> list[Player]:
        return await self.storage.players.lst()


# TODO: Refactor? Мне не нравится, что в Actions передается Request,
# который должен разбираться на уровне handler'a. Но тогда там нужно
# будет создавать все entities. Может, это и неплохо.


class CreatePlayersAction(AbstractAction[list[PlayerState]]):
    def __init__(self, request: CreatePlayersRequest) -> None:
        self.players = request.players

    async def handle(self) -> list[PlayerState]:
        ratings_state = await self.storage.ratings_states.get_actual()

        player_states: dict[_PlayerId, PlayerState] = {}

        for player_req in self.players:
            player = Player(
                id=None,
                first_name=player_req.first_name,
                last_name=player_req.last_name,
                city=player_req.city,
            )

            player = await self.storage.players.create(player)

            player_states[player.id] = await self.run_subaction(
                CreateInitialPlayerStateAction(
                    player=player,
                    evks_rating=player_req.initial_evks_rating,
                    cumulative_rating=player_req.initial_cumulative_rating,
                    matches_played=player_req.initial_matches_played,
                    matches_won=player_req.initial_matches_won,
                    is_evks_rating_active=player_req.is_evks_rating_active,
                )
            )

        new_state = replace(
            ratings_state,
            player_states=ratings_state.player_states.copy(),
            evks_player_ranks=ratings_state.evks_player_ranks.copy(),
        )

        new_state.player_states |= player_states

        await self.run_subaction(
            CreateRatingsStateAction(
                player_states=new_state.player_states,
                last_competition=ratings_state.last_competition,
            )
        )

        return player_states.values()
