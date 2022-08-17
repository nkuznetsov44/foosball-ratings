from common.handlers.abstract_handler import AbstractHandler


class AbstractDbHandler(AbstractHandler):
    @property
    def db(self):
        return self.app["db"]
