from types import TracebackType
from typing import Optional, Any, Type, TypeVar, Generic
from aiohttp import ClientSession, ClientResponse

from common.interactions.exceptions import InteractionResponseError


class BaseInteractionClient:
    _session: Optional[ClientSession] = None

    @property
    def session(self) -> ClientSession:
        if not self._session:
            self._session = ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session:
            await self._session.close()
        self._session = None

    async def _handle_response_error(self, resp: ClientResponse) -> None:
        response_text = None
        try:
            response_text = await resp.text()
        except:  # noqa: E722
            pass

        raise InteractionResponseError(
            request_url=resp.url,
            response_status=resp.status,
            response_text=response_text,
        )

    async def get(
        self, url: str, params: Optional[dict[str, Any]] = None
    ) -> Optional[dict[str, Any]]:
        if params:
            raise NotImplementedError
        async with self.session.get(url) as resp:
            if resp.status >= 400:
                await self._handle_response_error(resp)
            return await resp.json()

    async def post(
        self, url: str, data: Optional[dict[str, Any]] = None
    ) -> Optional[dict[str, Any]]:
        async with self.session.post(url, json=data) as resp:
            if resp.status >= 400:
                await self._handle_response_error(resp)
            return await resp.json()


InteractionClient = TypeVar("InteractionClient", bound=BaseInteractionClient)


class InteractionClientContext(Generic[InteractionClient]):
    client_cls: Type[InteractionClient]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._client = self.client_cls(*args, **kwargs)

    async def __aenter__(self) -> InteractionClient:
        return self._client

    async def __aexit__(self, exc_type: Type[Exception], exc: Exception, tb: TracebackType) -> None:
        await self._client.close()
