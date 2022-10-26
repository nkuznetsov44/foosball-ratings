from typing import Callable, Type
from json import JSONDecodeError
from typing import Any
from aiohttp import web
from marshmallow import Schema, ValidationError

from common.exceptions import MalformedRequest


def response_schema(schema: Type[Schema], many: bool = False) -> Callable[[Any], Any]:
    def decorator(handler_method: Any) -> Any:
        handler_method.response_schema = schema
        handler_method.response_schema_options = {"many": many}
        return handler_method

    return decorator


def request_schema(schema: Type[Schema]) -> Callable[[Any], Any]:
    def decorator(handler_method: Any) -> Any:
        handler_method.request_schema = schema
        return handler_method

    return decorator


class AbstractHandler(web.View):
    @property
    def app(self) -> web.Application:
        return self.request.app

    def _get_handler_method(self):
        handler_cls = self.request.match_info.handler
        return getattr(handler_cls, self.request.method.lower())

    async def get_request_data(self) -> Any:
        request_method = self.request.method.lower()
        schema_cls = self._get_handler_method().request_schema
        try:
            if request_method == "get":
                request_data = dict(self.request.rel_url.query) | dict(self.request.match_info)
                return schema_cls().load(request_data)
            elif request_method == "post":
                return schema_cls().load(await self.request.json())
            else:
                raise NotImplementedError(
                    f"Request method {request_method} not supported"
                )
        except JSONDecodeError as jde:
            raise MalformedRequest(reason=jde.msg)
        except ValidationError as ve:
            raise MalformedRequest(validation_errors=ve.messages)

    def make_response(self, response_data: Any) -> web.Response:
        schema_cls = self._get_handler_method().response_schema
        schema_options = self._get_handler_method().response_schema_options
        response = schema_cls(**schema_options).dump(response_data)
        return web.json_response(response)
