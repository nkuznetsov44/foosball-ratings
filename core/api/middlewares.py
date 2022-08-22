from aiohttp import web
from logging import getLogger
from core.exceptions import CoreProcessingError


logger = getLogger(__name__)


@web.middleware
async def core_processing_error_500_middleware(
    request: web.Request, handler: web.RequestHandler
) -> web.Response:
    try:
        return await handler(request)
    except CoreProcessingError as e:
        logger.exception("CORE_PROCESSING_ERROR")
        return web.json_response({"reason": e.reason, "params": e.params})
