from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.ds.frontier.i_0_base.main import FrontierBase

ULazy.install(globals(), {'FrontierBase': 'f_search.ds.frontier.i_0_base.main:FrontierBase'})
