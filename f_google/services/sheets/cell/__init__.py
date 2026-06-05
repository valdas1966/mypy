from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_google.services.sheets.cell.main import Cell

ULazy.install(globals(), {'Cell': 'f_google.services.sheets.cell.main:Cell'})
