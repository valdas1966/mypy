from f_data_structure.mixins.traversable import Traversable


class ContainerTraversable:

    def __init__(self,
                 elements: str    # Name of Elements in the SubClass
                 ) -> None:
        """
        ========================================================================
         Desc: Sets the Elements' Name in the SubClass.
        ========================================================================
        """
        self._elements = elements
        setattr(self, f'{elements}_traversable', self._elements_traversable)
        setattr(self, f'num_{elements}_traversable',
                self._num_elements_traversable)
        setattr(self, f'num_{elements}_non_traversable',
                self._num_elements_non_traversable)
        setattr(self, f'pct_{elements}_traversable',
                self._pct_elements_traversable)
        setattr(self, f'pct_{elements}_non_traversable',
                self._pct_elements_non_traversable)

    def _elements_traversable(self) -> list[Traversable]:
        """
        ========================================================================
         Desc: Return List of Traversable-Elements in the Container.
        ========================================================================
        """
        elements = getattr(self, self._elements)()
        return [ele for ele in elements if ele.is_traversable]



    def _num_elements_traversable(self) -> int:
        """
        ========================================================================
         Desc: Return Number of Traversable-Elements in the Container.
        ========================================================================
        """
        return len(self._elements_traversable())

    def _num_elements_non_traversable(self) -> int:
        """
        ========================================================================
         Desc: Returns a number of Non-Traversable-Elements in the Container.
        ========================================================================
        """
        num_elements_all = getattr(self, f'num_{self._elements}_all')()
        return num_elements_all - self._num_elements_traversable()

    def _pct_elements_traversable(self) -> float:
        """
        ========================================================================
         Desc: Returns a Percentage of Traversable-Elements in the Container.
        ========================================================================
        """
        num_elements_all = getattr(self, f'num_{self._elements}_all')()
        return self._num_elements_traversable() / num_elements_all

    def _pct_elements_non_traversable(self) -> float:
        """
        ========================================================================
         Desc: Returns a Percentage of Non-Traversable-Elements in the Container
        ========================================================================
        """
        num_elements_all = getattr(self, f'num_{self._elements}_all')()
        return self._num_elements_non_traversable() / num_elements_all
