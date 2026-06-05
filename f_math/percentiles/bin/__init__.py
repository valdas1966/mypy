from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_math.percentiles.bin.main import Bin

ULazy.install(globals(), {'Bin': 'f_math.percentiles.bin.main:Bin'})
