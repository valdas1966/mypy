from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for StateBase test instances.
    ========================================================================
    """

    @staticmethod
    def a() -> StateBase[str]:
        """
        ====================================================================
         Create a StateBase with key 'A'.
        ====================================================================
        """
        return StateBase[str](key='A')

    @staticmethod
    def b() -> StateBase[str]:
        """
        ====================================================================
         Create a StateBase with key 'B'.
        ====================================================================
        """
        return StateBase[str](key='B')
