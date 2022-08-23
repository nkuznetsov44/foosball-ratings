from typing import Type
from aiohttp import web
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from common.handlers import AbstractHandler, request_schema, response_schema
from webapp.entities.competition import Competition
from webapp.entities.player import Player
from webapp.schemas import (
    PlayerIdSchema,
    PlayerCompetitionIdSchema,
    GetPlayersResponseSchema,
    GetPlayerCompetitionsResponseSchema,
)


class AbstractWebappHandler(AbstractHandler):
    def make_db_session(self) -> Type[AsyncSession]:
        return sessionmaker(self.app["db"], expire_on_commit=False, class_=AsyncSession)


class GetPlayersHandler(AbstractWebappHandler):
    @response_schema(GetPlayersResponseSchema)
    async def get(self) -> web.Response:
        async with self.make_db_session()() as session:
            result = await session.execute(select(Player))
            players = result.scalars().all()
        return self.make_response({"players": players})


class GetPlayerCompetitionsHandler(AbstractWebappHandler):
    @request_schema(PlayerIdSchema)
    @response_schema(GetPlayerCompetitionsResponseSchema)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        async with self.make_db_session()() as session:
            # TODO: filter competitions by player
            # result = await session.execute(
            # select match.competition
            # where match.first_team.first_player.id == player_id
            # or ...
            # )

            # TODO: figure out how to get rid of selectinload option
            result = await session.execute(
                select(Competition).options(selectinload("*"))
            )
            competitions = result.scalars().all()
        return self.make_response({"competitions": competitions})


"""
class GetPlayerCompetitionMatchesHandler(AbstractWebappHandler):
    @request_schema(PlayerCompetitionIdSchema)
    @response_schema(GetPlayerCompetitionMatchesResponseSchema)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        pass
"""
