from .main import HasName


class Factory:
    """
    =======================================================================
     Factory for HasName object.
    =======================================================================
    """

    @staticmethod
    def a() -> HasName:
        """
        =======================================================================
         Return HasName object with name 'A'.
        =======================================================================
        """
        return HasName(name='A')
    
    @staticmethod
    def empty() -> HasName:
        """
        =======================================================================
         Return HasName object with empty name.
        =======================================================================
        """
        return HasName(name=str())
    
    @staticmethod
    def none() -> HasName:
        """
        =======================================================================
         Return HasName object with None name.
        =======================================================================
        """
        return HasName()
