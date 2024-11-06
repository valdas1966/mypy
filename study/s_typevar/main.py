from study.s_typevar.created_base import CreatedBase
from typing import Generic, TypeVar

Created = TypeVar('Created', bound=CreatedBase)


class Main(Generic[Created]):

    def __init__(self, created: Created) -> None:
        self.created = created
