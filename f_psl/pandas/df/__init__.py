from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_psl.pandas.df.main import UDf

ULazy.install(globals(), {'UDf': 'f_psl.pandas.df.main:UDf'})
