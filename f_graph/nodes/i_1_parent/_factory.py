from f_graph.nodes.i_1_parent.main import NodeParent


class Factory:
    """
    ============================================================================
     Factory for the NodeParent class.
    ============================================================================
    """

    @staticmethod
    def a() -> NodeParent[str]:
        """
        ========================================================================
         Create a new node with the key 'A'.
        ========================================================================
        """
        key = 'A'
        node = NodeParent[str](key=key)
        return node
    
    @staticmethod
    def b() -> NodeParent[str]:
        """
        ========================================================================
         Create a new node with the key 'B'.
        ========================================================================
        """
        node_a = Factory.a()
        key = 'B'
        node_b = NodeParent[str](key=key, parent=node_a)
        return node_b

    @staticmethod
    def c() -> NodeParent[str]:
        """
        ========================================================================
         Create a new node with the key 'C'.
        ========================================================================
        """
        node_b = Factory.b()
        key = 'C'
        node_c = NodeParent[str](key=key, parent=node_b)
        return node_c
        