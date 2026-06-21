from f_core.canonize import canonize
from f_core.mixins.has.key import HasKey
from f_core.mixins.has.row_col import HasRowCol


def test_canonize() -> None:
    """
    ========================================================================
     Test canonize() across the three dispatch branches:
       * primitives (int / str / None) pass through unchanged,
       * a HasKey object descends into its key,
       * a HasRowCol object descends into (row, col),
       * a nested keyed object (HasKey wrapping HasRowCol — the
         StateCell shape) fully descends to the leaf primitive,
       * tuple / list are canonized element-wise, type preserved,
       * the result is idempotent.
    ========================================================================
    """
    # Primitives pass through unchanged
    assert canonize(5) == 5
    assert canonize('A') == 'A'
    assert canonize(None) is None

    # HasKey object descends into its key
    assert canonize(HasKey(key='A')) == 'A'

    # HasRowCol object descends into (row, col)
    assert canonize(HasRowCol(row=0, col=0)) == (0, 0)

    # Nested keyed object (HasKey wrapping HasRowCol) — the
    # StateCell shape (StateBase[CellMap]) — fully descends
    nested = HasKey(key=HasRowCol(row=1, col=2))
    assert canonize(nested) == (1, 2)

    # tuple / list canonized element-wise, container type preserved
    states = (HasRowCol(0, 0), HasRowCol(1, 1))
    assert canonize(states) == ((0, 0), (1, 1))
    assert canonize([HasKey(key='A'), 3]) == ['A', 3]

    # Idempotent on the resulting primitive
    once = canonize(nested)
    assert canonize(once) == once
