from __future__ import annotations
from f_ds.nodes.i_0_uid import NodeUid, UID
from f_ds.nodes.mixins.has_hierarchy import HasHierarchy


class NodeHierarchy(NodeUid[UID], HasHierarchy):
    """
    ============================================================================
     Node Hierarchy Class.
    ============================================================================
    """

    def __init__(self,
                 uid: UID = None,
                 parent: NodeHierarchy = None,
                 name: str = 'NodeHierarchy') -> None:
        """
        ========================================================================
         Initialize the NodeHierarchy.
        ========================================================================
        """
        NodeUid.__init__(self, uid=uid, name=name)
        HasHierarchy.__init__(self, parent=parent)
