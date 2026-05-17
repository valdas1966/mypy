from f_core.imports import ULazy

ULazy.install(globals(), {
    'HasKey': 'f_core.mixins.has.key:HasKey',
    'HasName': 'f_core.mixins.has.name:HasName',
    'HasRowCol': 'f_core.mixins.has.row_col:HasRowCol',
    'HasRowsCols': 'f_core.mixins.has.rows_cols:HasRowsCols',
})
