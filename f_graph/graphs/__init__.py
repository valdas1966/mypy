from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .grid import GraphGrid

ULazy.install(globals(), {'GraphGrid': '.grid:GraphGrid'})
