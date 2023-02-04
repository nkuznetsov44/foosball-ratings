from dataclasses import replace

from common.entities.player import Player
from common.entities.player_state import PlayerState
from common.entities.ratings_state import PlayerStateSet
from core.actions.abstract_action import AbstractAction
from core.actions.player_state import CreateInitialPlayerStateAction
from core.actions.ratings_state import CreateRatingsStateAction
from common.interactions.core.requests.player import CreatePlayersRequest


class GetPlayerAction(AbstractAction[Player]):
    def __init__(self, player_id: int) -> None:
        self.player_id = player_id

    async def handle(self) -> Player:
        return await self.storage.players.get(self.player_id)


class GetPlayersAction(AbstractAction[list[Player]]):
    async def handle(self) -> list[Player]:
        return await self.storage.players.lst()


class CreatePlayersAction(AbstractAction[list[PlayerState]]):
    def __init__(self, create_players_request: CreatePlayersRequest) -> None:
        self.players = create_players_request.players

    async def handle(self) -> list[PlayerState]:
        ratings_state = await self.storage.ratings_states.get_actual()

        player_states: PlayerStateSet = PlayerStateSet()

        for player_req in self.players:
            player = Player(
                id=None,
                external_id=player_req.external_id,
                first_name=player_req.first_name,
                last_name=player_req.last_name,
                city=player_req.city,
                is_foreigner=player_req.is_foreigner,
            )

            player = await self.storage.players.create(player)

            player_states.add(
                await self.run_subaction(
                    CreateInitialPlayerStateAction(
                        player=player,
                        evks_rating=player_req.initial_evks_rating,
                        cumulative_rating=player_req.initial_cumulative_rating,
                        matches_played=player_req.initial_matches_played,
                        matches_won=player_req.initial_matches_won,
                        is_evks_rating_active=player_req.is_evks_rating_active,
                        ratings_state=ratings_state,
                    )
                )
            )

        new_state = replace(
            ratings_state,
            player_states=ratings_state.player_states,
        )

        new_state.player_states.update(player_states)

        await self.run_subaction(
            CreateRatingsStateAction(
                player_states=new_state.player_states,
                last_competition_id=ratings_state.last_competition_id,
            )
        )

        return player_states.to_list()
