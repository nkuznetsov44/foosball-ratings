from abc import ABC, abstractmethod
from typing import Any, Optional
from contextlib import asynccontextmanager

from storage.storage import StorageContext, Storage


class AbstractAction(ABC):
    storage_context = StorageContext

    def __init__(self) -> None:
        self.storage: Optional[Storage] = None

    @abstractmethod
    async def handle(self) -> Any:
        raise NotImplementedError()

    @asynccontextmanager
    async def _get_storage(self, storage: Optional[Storage] = None) -> Storage:
        if storage:
            yield storage
        else:
            async with self.storage_context() as storage:
                yield storage

    async def run(self, storage: Optional[Storage] = None) -> Any:
        async with self._get_storage(storage) as strg:
            self.storage = strg
            return await self.handle()

    async def run_subaction(self, action: 'AbstractAction') -> Any:
        return await action.run(self.storage)
