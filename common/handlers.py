from json import JSONDecodeError
from typing import Any
from aiohttp import web
from marshmallow import Schema, ValidationError
from common.exceptions import MalformedRequest


def response_schema(schema: Schema):
    def decorator(handler_method):
        handler_method.response_schema = schema
        return handler_method

    return decorator


def request_schema(schema: Schema):
    def decorator(handler_method):
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
        schema_cls = self._get_handler_method().request_schema
        try:
            return schema_cls().load(await self.request.json())
        except JSONDecodeError as jde:
            raise MalformedRequest(reason=jde.msg)
        except ValidationError as ve:
            raise MalformedRequest(validation_errors=ve.messages)

    def make_response(self, response_data: Any) -> web.Response:
        schema_cls = self._get_handler_method().response_schema
        response = schema_cls().dump(response_data)
        return web.json_response(response)
