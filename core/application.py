from aiohttp import web
from core.settings import config
from core.routes import setup_routes
from core.storage.db import pg_context


app = web.Application()
setup_routes(app)
app["config"] = config
app.cleanup_ctx.append(pg_context)


if __name__ == "__main__":
    web.run_app(app)
