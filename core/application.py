from aiohttp import web
from core.settings import config
from core.routes import setup_routes
from core.storage.db import setup_db_engine


app = web.Application()
setup_routes(app)
app["config"] = config
setup_db_engine(app)


if __name__ == "__main__":
    web.run_app(app)
