from f_search.generated.main import Generated, State, Cost


class Factory:
    """
    ============================================================================
     Factory for creating Generated objects.
    ============================================================================
    """

    @staticmethod
    def ab() -> Generated:
        """
        ========================================================================
         Create a Generated object with the 'A', 'B' states and mess inserted
          costs (A should be popped first even if B was pushed first).
        ========================================================================
        """
        state_a = State.Factory.zero()
        state_b = State.Factory.one()
        cost_a = Cost.Factory.a()
        cost_b = Cost.Factory.b()
        generated = Generated()
        generated.push(state=state_b, cost=cost_b)
        generated.push(state=state_a, cost=cost_a)
        return generated
