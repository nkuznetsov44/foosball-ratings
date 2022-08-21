from sqlalchemy import select
from core.actions.abstract_action import AbstractAction, ActionContext
from core.api.requests.player import CreatePlayersRequest
from core.entities.state import PlayerState
from core.entities.player import Player
from core.actions.state import CreateInitialPlayerStateAction, CreateRatingsStateAction


class GetPlayerAction(AbstractAction):
    def __init__(self, context: ActionContext, player_id: int) -> None:
        super().__init__(context)
        self._player_id = player_id

    async def run(self) -> Player:
        async with self._make_db_session()() as session:
            result = await session.execute(
                select(Player).where(Player.id == self._player_id)
            )
            return result.scalars().first()


class GetPlayersAction(AbstractAction):
    def __init__(self, context: ActionContext) -> None:
        super().__init__(context)

    async def run(self) -> list[Player]:
        async with self._make_db_session()() as session:
            result = await session.execute(select(Player))
            return result.scalars().all()


class CreatePlayersAction(AbstractAction):
    def __init__(self, request: CreatePlayersRequest, context: ActionContext) -> None:
        super().__init__(context)
        self._request = request

    async def run(self) -> set[PlayerState]:
        # TODO: transactional
        player_states: set[PlayerState] = set()

        for player_req in self._request.players:
            player = Player(
                first_name=player_req.first_name,
                last_name=player_req.last_name,
                city=player_req.city,
            )

            async with self._make_db_session()() as session:
                session.add(player)
                await session.commit()
                assert player.id is not None, "Player id is null after session commit"

            player_states.add(
                await self.run_action(
                    CreateInitialPlayerStateAction,
                    player=player,
                    evks_rating=player_req.initial_evks_rating,
                    cumulative_rating=player_req.initial_cumulative_rating,
                    matches_played=player_req.initial_matches_played,
                    matches_won=player_req.initial_matches_won,
                    is_evks_rating_active=player_req.is_evks_rating_active,
                )
            )

        new_state = self._ratings_state.dirty_copy()
        new_state.player_states.update(player_states)
        await self.run_action(
            CreateRatingsStateAction,
            player_states=player_states,
            last_competition=self._ratings_state.last_competition,
        )

        return player_states
