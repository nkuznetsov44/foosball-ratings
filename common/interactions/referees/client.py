from common.interactions.base import BaseInteractionClient, InteractionClientContext
from common.interactions.referees.entities import Referee
from common.interactions.referees.schemas import RefereeSchema


class RefereesClient(BaseInteractionClient):
    base_url = "https://foosref.nkuznetsov.com/api"  # TODO: to settings

    async def get_referees(self) -> list[Referee]:
        resp_json = await self.session.get(f"{self.base_url}/referees/")
        return RefereeSchema(many=True).load(resp_json)


class RefereesClientContext(InteractionClientContext[RefereesClient]):
    client_cls = RefereesClient
