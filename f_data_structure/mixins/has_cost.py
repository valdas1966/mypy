from __future__ import annotations


class HasCost:
    """
    ============================================================================
     Mixin Class for Objects with Cost-Function.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. cost() -> int
           [*] Returns the Object's Cost-Function Value.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. eq(other: HasCost) -> bool
        2. ne(other: HasCost) -> bool
        3. lt(other: HasCost) -> bool
        4. le(other: HasCost) -> bool
        5. gt(other: HasCost) -> bool
        6. ge(other: HasCost) -> bool
    ============================================================================
    """

    def cost(self) -> int | list[int]:
        """
        ========================================================================
         Returns the Object's Cost-Function Value.
        ========================================================================
        """
        raise NotImplementedError('Must implement cost() in subclass')

    def __eq__(self, other: HasCost) -> bool:
        return self.cost() == other.cost()

    def __ne__(self, other: HasCost) -> bool:
        return not self.cost() == other.cost()

    def __lt__(self, other: HasCost) -> bool:
        return self.cost() < other.cost()

    def __le__(self, other: HasCost) -> bool:
        return self.cost() <= other.cost()

    def __gt__(self, other: HasCost) -> bool:
        return self.cost() > other.cost()

    def __ge__(self, other: HasCost) -> bool:
        return self.cost() >= other.cost()
