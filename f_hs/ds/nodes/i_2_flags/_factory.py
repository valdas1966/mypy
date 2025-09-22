from f_hs.ds.nodes.i_2_flags.main import NodeFlags


class Factory:
    """
    ============================================================================
     Factory for the NodeFlags class.
    ============================================================================
    """
    
    @staticmethod
    def a() -> NodeFlags[str]:
        """
        ========================================================================
         Create a new node with the key 'a' and the h value 0.
        ========================================================================
        """
        node = NodeFlags(key='a', h=0)
        return node
        
    @staticmethod
    def b() -> NodeFlags[str]:
        """
        ========================================================================
         Create a new node with the key 'b' and the h value 5.
        ========================================================================
        """
        node = NodeFlags(key='b', h=5)
        node.is_cached = True
        node.is_bounded = True
        return node
    
    @staticmethod
    def c() -> NodeFlags[str]:
        """
        ========================================================================
         Create a new node with the key 'c' and the h value 5.
        ========================================================================
        """
        node = NodeFlags(key='c', h=5)
        node.is_cached = True
        node.is_bounded = False
        return node
        
    @staticmethod
    def d() -> NodeFlags[str]:
        """
        ========================================================================
         Create a new node with the key 'd' and the h value 5.
        ========================================================================
        """
        node = NodeFlags(key='d', h=5)
        return node
    
    @staticmethod
    def e() -> NodeFlags[str]:
        """
        ========================================================================
         Create a new node with the key 'e' and the h value 4.
        ========================================================================
        """
        node = NodeFlags(key='e', h=6)
        node._g = -1
        return node

    @staticmethod
    def f() -> NodeFlags[str]:
        """
        ========================================================================
         Create a new node with the key 'f' and the h value 4.
        ========================================================================
        """ 
        node = NodeFlags(key='f', h=6)
        node._g = -1
        return node
    