from f_ds.groups.main import Group


class Factory:
    """
    ============================================================================
     Factory for creating Group objects.
    ============================================================================
    """

    @staticmethod    
    def ab() -> Group[str]:
        """
        ========================================================================
         Return a Group with the 'a' and 'b' items.
        ========================================================================
        """
        data = ['a', 'b']
        return Group(data=data, name='AB')
    