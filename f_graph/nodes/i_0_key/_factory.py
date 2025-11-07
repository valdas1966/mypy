from f_graph.nodes.i_0_key.main import NodeKey


class Factory:
    """
    ============================================================================
     Factory for the NodeKey class.
    ============================================================================
    """

    @staticmethod
    def a() -> NodeKey:
        """
        ========================================================================
         Create a new node with the key 'A'.
        ========================================================================
        """
        key = 'A'
        return NodeKey[str](key=key)

    @staticmethod
    def b() -> NodeKey:
        """
        ========================================================================
         Create a new node with the key 'B'.
        ========================================================================
        """
        key = 'B'
        return NodeKey[str](key=key)
    