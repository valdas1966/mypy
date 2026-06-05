from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_cs.algo.main import Algo

ULazy.install(globals(), {'Algo': 'f_cs.algo.main:Algo'})
