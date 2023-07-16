
class Nameable:
    """
    ============================================================================
     Desc: Represents an Object with a Name property (Default=None).
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. name (str) : Object's Name.
    ============================================================================
    """

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
