from f_graph.path.algos.one_to_many.state import StateOneToMany


class GenStateOneToMany:
    """
    ============================================================================
     Generator of State-Objects for One-To-Many Path-Algorithms.
    ============================================================================
    """

    @staticmethod
    def gen_empty() -> StateOneToMany:
        """
        ========================================================================
         Generate an empty State-Object.
        ========================================================================
        """
        return StateOneToMany()
        