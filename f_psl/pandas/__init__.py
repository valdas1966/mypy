from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_psl.pandas.df import UDf
    from f_psl.pandas.csv import UCsv

ULazy.install(globals(), {
    'UDf': 'f_psl.pandas.df:UDf',
    'UCsv': 'f_psl.pandas.csv:UCsv',
})
