from core.handlers.abstract_handler import AbstractHandler

class CreatePlayerStateHandler(AbstractHandler[CreatePlayerStateAction]):
    async def handle(self, action: CreatePlayerStateAction) -> PlayerState:
        pass


class CreateRatingsStateHandler(AbstractHandler[CreateRatingsStateAction]):
    async def handle(self, action: CreateRatingsStateAction) -> RatingsState:
        pass
