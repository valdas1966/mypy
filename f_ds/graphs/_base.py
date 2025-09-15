from __future__ import annotations
from f_core.mixins.has.name import HasName
from f_core.mixins.clonable import Clonable
from f_core.mixins.equable import Equable
from f_ds.mixins.groupable import Groupable, Group
from f_ds.nodes.i_0_key import NodeKey
from typing import TypeVar, Generic, Self
from abc import abstractmethod

Node = TypeVar('Node', bound=NodeKey)


class GraphBase(Generic[Node],
                Groupable[Node],
                HasName,
                Clonable,
                Equable):
    """
    ============================================================================
     Graph Base-Class.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name)

    @abstractmethod
    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Return List of Nodes in the Graph.
        ========================================================================
        """
        pass

    @abstractmethod
    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns List of given Node's neighbors.
        ========================================================================
        """
        pass

    @abstractmethod
    def clone(self) -> Self:
        """
        ========================================================================
         Return a Cloned object.
        ========================================================================
        """
        pass

    def key_comparison(self) -> ProtocolEquable:
        """
        ========================================================================
         Return a Key-Comparison object.
        ========================================================================
        """
        pass

    def to_group(self, name: str = None) -> Group[Node]:
        """
        ========================================================================
         Return a Group representation of the Object.
        ========================================================================
        """
        return Group(name=name, data=self.nodes())
