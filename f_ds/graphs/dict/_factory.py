from f_ds.graphs.dict.main import GraphDict
from f_ds.nodes.i_0_key import NodeKey


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
         Create a GraphDict object with the 'a', 'b', 'c' nodes.
        ========================================================================
        """
        a = NodeKey(key='A')
        b = NodeKey(key='B')
        c = NodeKey(key='C')
        data = {'a': a, 'b': b, 'c': c}
        return GraphDict(data=data)
