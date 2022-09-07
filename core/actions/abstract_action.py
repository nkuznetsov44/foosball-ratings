from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Generic, TypeVar
from contextlib import asynccontextmanager

from storage.storage import StorageContext, Storage


ActionResult = TypeVar("ActionResult")
SubActionResult = TypeVar("SubActionResult")


class AbstractAction(Generic[ActionResult], metaclass=ABCMeta):
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

    async def run(self, storage: Optional[Storage] = None) -> ActionResult:
        async with self._get_storage(storage) as strg:
            self.storage = strg
            return await self.handle()

    async def run_subaction(
        self, action: "AbstractAction[SubActionResult]"
    ) -> SubActionResult:
        return await action.run(self.storage)
