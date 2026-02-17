from __future__ import annotations


class HasName:
    """
    ============================================================================
     Mixin with Name property (Default='None').
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self, name: str = 'NoName') -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        assert isinstance(name, str), f'Name must be a string, got {type(name)}'
        self._name = name

    @property
    # Object's Name
    def name(self) -> str:
        """
        ========================================================================
         Return the object's name.
        ========================================================================
        """
        return self._name

    def __str__(self) -> str:
        """
        ========================================================================
         Return object string representation.
        ========================================================================
        """
        return self.name

    def __repr__(self) -> str:
        """
        ========================================================================
         Return object representation.
        ========================================================================
        """
        return f'<{type(self).__name__}: Name={self.name}>'
