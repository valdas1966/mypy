
class Nameable:
    """
    ============================================================================
     Mixin with a Name property (Default=None).
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. str -> 'name' or '' if None
        2. repr -> str
    ============================================================================
    """

    _name: str               # Object's Name

    def __init__(self, name: str = None) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def __str__(self) -> str:
        return self.name if self.name else ''

    def __repr__(self) -> str:
        return self.__str__()
