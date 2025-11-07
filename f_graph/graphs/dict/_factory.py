from f_graph.graphs.dict.main import GraphDict
from f_graph.nodes.i_0_key import NodeKey


class Factory:
    """
    ============================================================================
     Factory for creating GraphDict objects.
    ============================================================================
    """

    @staticmethod
    def abc() -> GraphDict:
        """
        ========================================================================
         Create a GraphDict object with the 'a', 'b', 'c' old_nodes.
        ========================================================================
        """
        a = NodeKey(key='A')
        b = NodeKey(key='B')
        c = NodeKey(key='C')
        data = {'a': a, 'b': b, 'c': c}
        return GraphDict(data=data)
