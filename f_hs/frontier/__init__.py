from f_core.imports import ULazy

ULazy.install(globals(), {
    'FrontierBase': 'f_hs.frontier.i_0_base:FrontierBase',
    'FrontierFIFO': 'f_hs.frontier.i_1_fifo:FrontierFIFO',
    'FrontierPriority': 'f_hs.frontier.i_1_priority:FrontierPriority',
})
