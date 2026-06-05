from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_psl.pandas.csv.main import UCsv

ULazy.install(globals(), {'UCsv': 'f_psl.pandas.csv.main:UCsv'})
