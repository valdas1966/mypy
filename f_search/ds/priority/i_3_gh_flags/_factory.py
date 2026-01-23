from f_search.ds.priority.i_3_gh_flags.main import PriorityGHFlags


class Factory:
    """
    ============================================================================
     Factory for the PriorityGHFlags class.
    ============================================================================
    """

    @staticmethod
    def cached() -> PriorityGHFlags:
        """
        ========================================================================    
         Create a new PriorityGHFlags cached object.  
        ========================================================================
        """
        key = 'A'
        g = 1
        h = 2
        is_cached = True
        is_bounded = False
        return PriorityGHFlags(key, g, h, is_cached, is_bounded)

    @staticmethod
    def bounded() -> PriorityGHFlags:
        """
        ========================================================================
         Create a new PriorityGHFlags bounded object.
        ========================================================================
        """
        key = 'A'
        g = 1
        h = 2
        is_cached = False
        is_bounded = True
        return PriorityGHFlags(key, g, h, is_cached, is_bounded)

    @staticmethod
    def regular() -> PriorityGHFlags:
        """
        ========================================================================
         Create a new PriorityGHFlags regular object.
        ========================================================================
        """
        key = 'A'
        g = 1
        h = 2
        is_cached = False
        is_bounded = False
        return PriorityGHFlags(key, g, h, is_cached, is_bounded)
        