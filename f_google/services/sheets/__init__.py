from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_google.services.sheets.spread import Spread
    from f_google.services.sheets.sheet import Sheet
    from f_google.services.sheets.cell import Cell

ULazy.install(globals(), {
    'Spread': 'f_google.services.sheets.spread:Spread',
    'Sheet': 'f_google.services.sheets.sheet:Sheet',
    'Cell': 'f_google.services.sheets.cell:Cell',
})
