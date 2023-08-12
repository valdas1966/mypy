
class MixinEven:

    def __init__(self,
                 func_elements: str) -> None:
        self._func_elements = func_elements
        setattr(self, f'{func_elements}_even', self._elements_even)

    def _elements_even(self) -> list[int]:
        elements = getattr(self, self._func_elements)()
        return [ele for ele in elements if ele % 2 == 0]
