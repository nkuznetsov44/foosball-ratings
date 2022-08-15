from core.storage.abstract_storage import AbstractRatingStateStorage

class CoreApplication:
    def __init__(self, storage: AbstractRatingStateStorage) -> None:
        self.storage = storage
        self.current_state = storage.get_current_state()


storage = AbstractRatingStateStorage()  # init storage here
app = CoreApplication(storage)
