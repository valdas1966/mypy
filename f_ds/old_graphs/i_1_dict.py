from __future__ import annotations
from f_ds.old_graphs.i_0_base import GraphBase
from f_graph.nodes import NodeKey, Key
from f_core.mixins.equable import Equable
from typing import Generic,Type, TypeVar, Iterable

Node = TypeVar('Node', bound=NodeKey)


class GraphDict(Generic[Node], GraphBase[Node], Equable):
    """
    ============================================================================
     Dict-Based Graph.
    ============================================================================
    """

    def __init__(self,
                 keys: Iterable[Key],
                 type_node: Type[Node] = NodeKey,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GraphBase.__init__(self, name=name)
        self._nodes: dict[Key, Node] = {key: type_node(key=key)
                                        for key
                                        in keys}

    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Return a List of Graph's Nodes.
        ========================================================================
        """
        return list(self._nodes.values())

    def nodes_by_keys(self,
                      key: Key = None,
                      keys: Iterable[Key] = None) -> Node | list[Node]:
        """
        ========================================================================
         Return a Node by a given UID.
        ========================================================================
        """
        if key:
            return self._nodes[key]
        elif keys:
            return [self._nodes[key] for key in keys]
        return None

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return a List of given Node's neighbors.
        ========================================================================
        """
        return list()
    
    def clone(self) -> GraphDict:
        """
        ========================================================================
         Return a Cloned object.
        ========================================================================
        """
        keys = list(self._nodes.keys())
        return GraphDict(keys=keys,
                         type_node=type(self._nodes[keys[0]]),
                         name=self.name)

    def key_comparison(self) -> dict:
        """
        ========================================================================
         Compare by a Dict of Nodes.
        ========================================================================
        """
        return self._nodes
