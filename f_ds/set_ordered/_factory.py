from f_ds.set_ordered.main import SetOrdered


class Factory:
    """
    ========================================================================
     Factory for creating SetOrdered instances.
    ========================================================================
    """

    @staticmethod
    def abc() -> SetOrdered[str]:
        """
        ====================================================================
         Create a SetOrdered with ['a', 'b', 'c'].
        ====================================================================
        """
        return SetOrdered(['a', 'b', 'c'])
