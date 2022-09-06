from dataclasses import dataclass, field
from uuid import UUID, uuid4


def generate_uuid() -> UUID:
    return uuid4


@dataclass
class BaseRequest:
    request_id: UUID = field(default_factory=generate_uuid)
