from aiohttp import web
from common.exceptions import MalformedRequest


@web.middleware
async def malformed_request_400_middleware(
    request: web.Request, handler: web.RequestHandler
) -> web.Response:
    try:
        return await handler(request)
    except MalformedRequest as mr:
        return web.json_response(
            status=400,
            data={"reason": mr.reason, "validation_errors": mr.validation_errors},
        )
