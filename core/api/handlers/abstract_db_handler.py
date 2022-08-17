from aiopg.sa.engine import Engine
from common.handlers.abstract_handler import AbstractHandler


class AbstractDbHandler(AbstractHandler):
    @property
    def db(self) -> Engine:
        return self.app["db"]
