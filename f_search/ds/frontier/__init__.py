from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.ds.frontier.i_0_base import FrontierBase
    from f_search.ds.frontier.i_1_fifo import FrontierFifo
    from f_search.ds.frontier.i_1_priority import FrontierPriority

ULazy.install(globals(), {
    'FrontierBase': 'f_search.ds.frontier.i_0_base:FrontierBase',
    'FrontierFifo': 'f_search.ds.frontier.i_1_fifo:FrontierFifo',
    'FrontierPriority': 'f_search.ds.frontier.i_1_priority:FrontierPriority',
})
