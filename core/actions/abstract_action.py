from typing import Any
from abc import ABC, abstractmethod


class AbstractAction(ABC):
    @abstractmethod
    async def run(self) -> Any:
        raise NotImplementedError()
