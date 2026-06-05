from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.mixins.has.key import HasKey
    from f_core.mixins.has.name import HasName
    from f_core.mixins.has.row_col import HasRowCol
    from f_core.mixins.has.rows_cols import HasRowsCols

ULazy.install(globals(), {
    'HasKey': 'f_core.mixins.has.key:HasKey',
    'HasName': 'f_core.mixins.has.name:HasName',
    'HasRowCol': 'f_core.mixins.has.row_col:HasRowCol',
    'HasRowsCols': 'f_core.mixins.has.rows_cols:HasRowsCols',
})
