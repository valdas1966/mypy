from f_core.abstracts.dictable import Dictable
from dataclasses import dataclass, field
from typing import Generic, TypeVar

DATA = TypeVar('DATA', bound=Dictable)


@dataclass
class DataResponse(Generic[DATA], Dictable):
    """
    ============================================================================
     DataClass for Response from Tiktok-API.
    ============================================================================
    """
    is_ok = bool
    is_found = bool
    data: DATA = field(default=None)

    def to_dict(self) -> dict:
        """
        ========================================================================
         Convert the Data-Class into a Dict.
        ========================================================================
        """
        d: dict[str, any] = dict()
        d['is_ok'] = DataResponse.is_ok
        d['is_found'] = DataResponse.is_found
        d.update(DataResponse.data.to_dict())
        return d
