from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.frontier.i_0_base.main import FrontierBase

ULazy.install(globals(), {'FrontierBase': 'f_hs.frontier.i_0_base.main:FrontierBase'})
