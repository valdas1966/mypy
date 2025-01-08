from __future__ import annotations
from f_ds.nodes.i_0_uid import NodeUid, UID
from f_ds.nodes.mixins.has_g import HasG
from f_ds.nodes.mixins.has_h import HasH


class NodeHeuristic(NodeUid[UID], HasG, HasH):
    """
    ============================================================================
     NodeGraph with Path functionality.
    ============================================================================
    """

    def __init__(self,
                 uid: UID,
                 parent: NodeHeuristic = None,
                 h: int = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeUid.__init__(self, uid=uid, name=name)
        HasG.__init__(self, parent=parent)
        HasH.__init__(self, h=h)
        self._is_cached: bool = False

    def set_cached(self) -> None:
        """
        ========================================================================
         Mark a Node as Cached (known the accurate path to the Goal).
        ========================================================================
        """
        self._is_cached = True

    def f(self) -> int:
        """
        ========================================================================
         Return a Heuristic-Distance from Node to the Goal.
        ========================================================================
        """
        return (self.g + self.h) if self.h else self.g

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare between Nodes by: F, H, UID.
        ========================================================================
        """
        return [self.f(), not self._is_cached, self.h, self.uid]

    @classmethod
    def generate_zero(cls) -> NodeHeuristic:
        """
        ========================================================================
         Generate a Node with UID=0, H=0.
        ========================================================================
        """
        return cls[int](uid=0, h=0)
    
    @classmethod
    def generate_branch(cls, depth: int) -> list[NodeHeuristic]:
        """
        ========================================================================
         Generate a Branch of Nodes.
        ========================================================================
        """
        branch: list[NodeHeuristic] = []
        for i in range(depth):
            node = NodeHeuristic[int](uid=i)
            if i > 0:
                node.parent = branch[i - 1]
            branch.append(node)
        return branch

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-Representation of the Node.
        ------------------------------------------------------------------------
         Ex: '<NodePath: (0,0), g=2, h=3, f=5>'
        ========================================================================
        """
        return f'uid={self.uid}, g={self.g}, h={self.h}, f={self.f()}'
