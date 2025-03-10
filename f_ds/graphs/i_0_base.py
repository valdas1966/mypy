from __future__ import annotations
from abc import abstractmethod
from typing import TypeVar, Generic
from f_core.mixins.has_name import HasName
from f_core.abstracts.clonable import Clonable
from f_ds.mixins.groupable import Groupable, Group
from f_ds.nodes.i_0_key import NodeKey

Node = TypeVar('Node', bound=NodeKey)


class GraphBase(Generic[Node], Groupable[Node], HasName, Clonable):
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
    def clone(self) -> GraphBase:
        """
        ========================================================================
         Return a Cloned object.
        ========================================================================
        """
        pass
    
    def to_group(self, name: str = None) -> Group[Node]:
        """
        ========================================================================
         Return list list representation of the Object.
        ========================================================================
        """
        return Group(name=name, data=self.nodes())
