from aiohttp import web
from core.exceptions import CoreProcessingError


@web.middleware
async def core_processing_error_500_middleware(
    request: web.Request, handler: web.RequestHandler
) -> web.Response:
    try:
        return await handler(request)
    except CoreProcessingError as e:
        return handler.make_error_response(e)
