from f_core.imports import ULazy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f_core.mixins.has.key import HasKey
    from f_core.mixins.has.name import HasName
    from f_core.mixins.has.repr import HasRepr
    from f_core.mixins.has.row_col import HasRowCol
    from f_core.mixins.has.rows_cols import HasRowsCols

ULazy.install(globals(), {
    'HasKey': 'f_core.mixins.has.key:HasKey',
    'HasName': 'f_core.mixins.has.name:HasName',
    'HasRepr': 'f_core.mixins.has.repr:HasRepr',
    'HasRowCol': 'f_core.mixins.has.row_col:HasRowCol',
    'HasRowsCols': 'f_core.mixins.has.rows_cols:HasRowsCols',
})
