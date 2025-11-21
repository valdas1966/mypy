from f_graph.old_path.algos.one_to_many.state import StateOneToMany


class GenStateOneToMany:
    """
    ============================================================================
     Generator of StateBase-Objects for One-To-Many Path-Algorithms.
    ============================================================================
    """

    @staticmethod
    def gen_empty() -> StateOneToMany:
        """
        ========================================================================
         Generate an empty StateBase-Object.
        ========================================================================
        """
        return StateOneToMany()
        