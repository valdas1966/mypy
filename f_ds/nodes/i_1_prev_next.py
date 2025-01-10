from f_ds.nodes.i_0_uid import NodeUid, UID
from f_ds.nodes.mixins.has_prev_next import HasPrevNext


class NodePrevNext(NodeUid[UID], HasPrevNext['NodePrevNext']):
    """
    ============================================================================
     A node with a previous and next object.
    ============================================================================
    """

    def __init__(self, uid: UID, name: str = None) -> None:
        """
        ========================================================================
         Initialize the node.
        ========================================================================
        """
        NodeUid.__init__(self, uid=uid, name=name)
        HasPrevNext.__init__(self)
