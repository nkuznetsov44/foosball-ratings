from aiohttp import web
from common.handlers.abstract_handler import request_schema, response_schema
from core.api.handlers.abstract_db_handler import AbstractDbHandler
from core.api.requests.schemas import (
    CreatePlayersRequestSchema,
    CreatePlayersResponseSchema,
    GetPlayersResponseSchema,
)
from core.api.requests.player import CreatePlayersRequest
from core.entities.state import PlayerState
from core.entities.player import Player
from core.actions.player import CreatePlayersAction


class PlayersHandler(AbstractDbHandler):
    @response_schema(GetPlayersResponseSchema)
    async def get(self) -> web.Response:
        async with self.db.acquire() as conn:
            cursor = await conn.execute(Player.table.select())
            records = await cursor.fetchall()
            return self.make_response({"players": records})

    @request_schema(CreatePlayersRequestSchema)
    # @response_schema(CreatePlayersResponseSchema)
    @response_schema(GetPlayersResponseSchema)
    async def post(self) -> web.Response:
        # action = CreatePlayersAction(request)
        # player_states = await action.run()
        # return self.make_response({
        #    "players": players
        # })

        create_players_request = await self.get_request_data()

        async with self.db.acquire() as conn:
            for player in create_players_request.players:
                await conn.execute(
                    Player.table()
                    .insert()
                    .values(first_name=player.first_name, last_name=player.last_name)
                )

                cursor = await conn.execute(Player.table().select())
                player_entities = await cursor.fetchall()

                return self.make_response({"players": player_entities})

        return web.Response("text")
