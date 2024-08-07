# .... = f_cs
from .....f_ds.nodes.i_1_path import NodePath
from .....f_ds.collections.i_1_queue import QueueBase
from f_graph.problems.i_0_graph
from typing import Generic, TypeVar
from abc import ABC

Queue = TypeVar('Queue', bound=QueueBase)
Node = TypeVar('Node', bound=NodePath)

class AlgoPathFinding(ABC, Generic[Queue, Node]):

    def __init__(self):