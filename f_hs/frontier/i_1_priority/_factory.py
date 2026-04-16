from f_hs.frontier.i_1_priority.main import FrontierPriority


class Factory:
    """
    ========================================================================
     Factory for FrontierPriority test instances.
    ========================================================================
    """

    @staticmethod
    def empty() -> FrontierPriority[str]:
        """
        ====================================================================
         Empty FrontierPriority.
        ====================================================================
        """
        return FrontierPriority[str]()

    @staticmethod
    def abc() -> FrontierPriority[str]:
        """
        ====================================================================
         FrontierPriority with A(3), B(1), C(2) — pops B, C, A.
        ====================================================================
        """
        f = FrontierPriority[str]()
        f.push(state='A', priority=(3,))
        f.push(state='B', priority=(1,))
        f.push(state='C', priority=(2,))
        return f
