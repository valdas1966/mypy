from f_core.components.data import Data, dataclass, field
from f_ds.queues.i_0_base import QueueBase as Queue
from f_graph.path.elements.node import NodePath
from typing import Generic, TypeVar, Type

Node = TypeVar('Node', bound=NodePath)


@dataclass
class State(Generic[Node], Data):
    """
    ============================================================================
     State object of Path-Finding Algorithms.
    ============================================================================
    """
    type_queue: Type[Queue]
    generated: Queue[Node] = field(init=False)
    explored: set[Node] = field(default_factory=set)
    best: Node = field(default=None)

    def __post_init__(self) -> None:
        self.generated = self.type_queue()
