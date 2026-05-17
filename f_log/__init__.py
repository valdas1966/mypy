from f_core.imports import ULazy

ULazy.install(globals(), {
    'setup_log': 'f_log.u_log:setup_log',
    'get_log': 'f_log.u_log:get_log',
    'ColorLog': 'f_log.color_log:ColorLog',
    'log_func': 'f_log.u_decorator:log_func',
})
