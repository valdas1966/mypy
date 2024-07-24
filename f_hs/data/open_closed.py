from f_ds.queues.i_0_base import QueueBase
from typing import Generic, TypeVar

Q = TypeVar('Q', bound=QueueBase)


class OpenClosed(Generic[Q]):

    def __init__(self) -> None:
