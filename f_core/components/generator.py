from typing import Generic, TypeVar, Type

Class = TypeVar('Class')


class Generator(Generic[Class]):
    """
    ============================================================================
     Component-Class of Class-Generator.
    ============================================================================
    """

    def __init__(self, type_class: Type[Class]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._type_class = type_class
