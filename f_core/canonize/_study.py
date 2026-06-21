"""
Toy examples for `canonize`. Run:

    python -m f_core.canonize._study

`canonize(v)` collapses any keyed framework object to a clean
primitive identity (tuple / int / str / ...), recursively.
"""
from f_core.canonize import canonize
from f_core.mixins.has.key import HasKey
from f_core.mixins.has.row_col import HasRowCol


# 1) Primitives pass straight through.
print(canonize(42))                          # 42
print(canonize('A'))                         # A
print(canonize(None))                        # None

# 2) A keyed object collapses to its key.
print(canonize(HasKey(key='A')))             # A
print(canonize(HasRowCol(row=0, col=0)))     # (0, 0)

# 3) Nested keyed object — the StateCell shape (a key whose value
#    is itself a keyed object) fully descends to the leaf tuple.
cell_state = HasKey(key=HasRowCol(row=1, col=2))
print(canonize(cell_state))                  # (1, 2)

# 4) Containers are walked element-wise, container type preserved.
frontier = (HasRowCol(0, 0), HasRowCol(1, 1), HasRowCol(2, 2))
print(canonize(frontier))                    # ((0, 0), (1, 1), (2, 2))
print(canonize([HasKey(key='A'), 3, None]))  # ['A', 3, None]

# 5) Idempotent — canonizing a primitive returns it unchanged.
once = canonize(cell_state)
print(canonize(once) == once)                # True
