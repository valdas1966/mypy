from f_core.mixins.has.parent.main import HasParent
from f_core.mixins.has.name import HasName


class ParentWithName(HasParent, HasName):
    """
    ========================================================================
     A parent with a name.
    ========================================================================
    """

    def __init__(self, name: str, parent: HasParent = None) -> None:
        HasParent.__init__(self, parent=parent)
        HasName.__init__(self, name=name)

class Factory:
    """
    ============================================================================
     Factory for the HasParent class.
    ============================================================================
    """

    @staticmethod
    def a() -> ParentWithName:
        """
        ========================================================================
         Return a HasParent object without a parent.
        ========================================================================
        """
        return ParentWithName(name='A')
    
    @staticmethod
    def b() -> ParentWithName:
        """
        ========================================================================
         Return a HasParent object with a parent 'a'.
        ========================================================================
        """
        a = Factory.a()
        return ParentWithName(name='B', parent=a)
