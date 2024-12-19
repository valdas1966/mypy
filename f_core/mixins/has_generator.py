from f_core.components.generator import Generator
from typing import Generic, TypeVar

Class = TypeVar('Class')


class HasGenerator(Generic[Class]):
    """
    ============================================================================
     Mixin for Classes with Class-Generator.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._gen: Generator[Class] = None

    @property
    def gen(self) -> Generator:
        return self._gen

    @gen.setter
    def gen(self, gen: Generator) -> None:
        self._gen = gen

