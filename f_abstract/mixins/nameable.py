from __future__ import annotations


class Nameable:
    """
    ============================================================================
     Mixin with a Name property (Default=None).
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. str -> 'name' or '' if None
        2. repr -> str
        3. eq -> bool
        4. ne -> bool
        5. hash -> int
    ============================================================================
    """

    _name: str               # Object's Name

    def __init__(self, name: str = None) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.name if self.name else ''

    def __repr__(self) -> str:
        return f'<{type(self).__name__}: {self.__str__()}>'

    def __eq__(self, other: Nameable) -> bool:
        return self.name == other.name and self.name is not None

    def __ne__(self, other: Nameable) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.name)
