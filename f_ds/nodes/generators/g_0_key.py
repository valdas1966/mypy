from f_ds.nodes.i_0_key import NodeKey, Key


class GenNodeKey:
    """
    ============================================================================
     Generator for NodeKey.
    ============================================================================
    """

    @staticmethod
    def one() -> NodeKey[Key]:
        """
        ========================================================================
         Generate a NodeKey.
        ========================================================================
        """
        key = 1
        name = 'One'
        return NodeKey[int](key=key, name=name)

