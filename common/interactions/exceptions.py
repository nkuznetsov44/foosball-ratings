from typing import Optional


class InteractionResponseError(Exception):
    def __init__(
        self,
        request_url: str,
        response_status: int,
        response_text: Optional[str],
    ) -> None:
        self.request_url = request_url
        self.response_status = response_status
        self.response_text = response_text

    def __str__(self) -> str:
        return (
            f"InteractionResponseError(url={self.request_url}, "
            f"status={self.response_status}):\n{self.response_text}"
        )
