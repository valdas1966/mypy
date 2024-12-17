from f_core.components.generator import Generator
from typing import Generic, TypeVar

Class = TypeVar('Class')


class HasGenerator(Generic[Class]):

    def __init__(self) -> None:
        self._generator = Generator[Class]()

    @property
    def generator(self) -> Generator:
        return self._generator

