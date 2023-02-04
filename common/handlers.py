from dataclasses import dataclass
from enum import Enum, unique
from typing import Callable, Type
from json import JSONDecodeError
from typing import Any
from aiohttp import web
from marshmallow import Schema, ValidationError

from common.exceptions import MalformedRequest
from common.utils import camel_to_snake


@unique
class RequestSchemaLocation(Enum):
    JSON = "json"
    MATCH_INFO = "match_info"
    QUERY = "query"


@dataclass
class RequestSchema:
    schema: Type[Schema]
    location: RequestSchemaLocation


@dataclass
class ResponseSchema:
    schema: Type[Schema]
    options: dict[str, Any]


def response_schema(schema: Type[Schema], many: bool = False) -> Callable[[Any], Any]:
    def decorator(handler_method: Any) -> Any:
        handler_method.response_schema = ResponseSchema(schema=schema, options=dict(many=many))
        return handler_method

    return decorator


def request_schema(schema: Type[Schema], *, location: str) -> Callable[[Any], Any]:
    def decorator(handler_method: Any) -> Any:
        request_schema = RequestSchema(schema=schema, location=RequestSchemaLocation(location))
        if hasattr(handler_method, "request_schemas"):
            handler_method.request_schemas.append(request_schema)
        else:
            handler_method.request_schemas = [request_schema]
        return handler_method

    return decorator


class AbstractHandler(web.View):
    @property
    def app(self) -> web.Application:
        return self.request.app

    def _get_handler_method(self):
        handler_cls = self.request.match_info.handler
        return getattr(handler_cls, self.request.method.lower())

    async def get_request_data(self) -> dict[str, Any]:
        handler = self._get_handler_method()
        if not hasattr(handler, "request_schemas"):
            raise NotImplementedError("Handler should be decorated with @request_schema")
        request_schemas: list[RequestSchema] = handler.request_schemas

        parsed: dict[str, Any] = dict()
        for request_schema in request_schemas:
            match request_schema.location:
                case RequestSchemaLocation.QUERY:
                    request_data = dict(self.request.rel_url.query)
                case RequestSchemaLocation.MATCH_INFO:
                    request_data = dict(self.request.match_info)
                case RequestSchemaLocation.JSON:
                    try:
                        request_data = await self.request.json()
                    except JSONDecodeError as jde:
                        raise MalformedRequest(reason=jde.msg)
            parsed |= self._parse_request_data(
                schema=request_schema.schema, request_data=request_data
            )
        return parsed

    def _parse_request_data(
        self, schema: Type[Schema], request_data: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            data = schema().load(request_data)
        except ValidationError as ve:
            raise MalformedRequest(validation_errors=ve.messages)

        if isinstance(data, dict):
            return data
        return {camel_to_snake(type(data).__name__): data}

    def make_response(self, response_data: Any) -> web.Response:
        handler = self._get_handler_method()
        if not hasattr(handler, "response_schema"):
            raise NotImplementedError("Handler should be decorated with @response_schema")
        response_schema: ResponseSchema = handler.response_schema
        response = response_schema.schema(**response_schema.options).dump(response_data)
        return web.json_response(response)
