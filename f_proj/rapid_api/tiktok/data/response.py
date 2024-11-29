from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclass
class DataResponse(Generic[T]):
    """
    ============================================================================
     DataClass for Response from Tiktok-API.
    ============================================================================
    """
    is_succeed = bool
    is_found = bool
    data: T = field(default=None)
