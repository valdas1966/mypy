from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_google.services.sheets.sheet.main import Sheet

ULazy.install(globals(), {'Sheet': 'f_google.services.sheets.sheet.main:Sheet'})
