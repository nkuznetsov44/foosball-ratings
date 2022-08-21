from typing import Optional, Any


class MalformedRequest(Exception):
    DEFAULT_REASON = "Request data is not valid"

    def __init__(
        self,
        reason: Optional[str] = None,
        validation_errors: Optional[dict[str, Any]] = None,
    ) -> None:
        reason = reason or self.DEFAULT_REASON
        super().__init__(reason)
        self.reason = reason
        self.validation_errors = validation_errors
