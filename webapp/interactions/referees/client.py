import aiohttp

from webapp.interactions.base import BaseInteractionClient
from webapp.interactions.referees.entities import Referee
from webapp.interactions.referees.schemas import RefereeSchema


class RefereesClient(BaseInteractionClient):
    base_url = "https://foosref.nkuznetsov.com/api"  # TODO: to settings

    async def get_referees(self) -> list[Referee]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/referees/") as resp:
                resp_json = await resp.json()
                return RefereeSchema(many=True).load(resp_json)
