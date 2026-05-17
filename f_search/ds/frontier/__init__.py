from f_core.imports import ULazy

ULazy.install(globals(), {
    'FrontierBase': 'f_search.ds.frontier.i_0_base:FrontierBase',
    'FrontierFifo': 'f_search.ds.frontier.i_1_fifo:FrontierFifo',
    'FrontierPriority': 'f_search.ds.frontier.i_1_priority:FrontierPriority',
})
