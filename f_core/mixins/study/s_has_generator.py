from f_core.components.generator import Generator
from f_core.mixins.has_generator import HasGenerator
from typing import Type


class GenA(Generator['A']):

    def __init__(self, type_class: Type['A']) -> None:
        Generator.__init__(self, type_class=type_class)

    def red(self) -> 'A':
        return self._type_class(value=1)


class A(HasGenerator['A']):

    def __init__(self, value: int) -> None:
        HasGenerator.__init__(self)
        self.value = value
        self.gen = GenA

