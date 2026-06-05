from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_log.u_log import setup_log
    from f_log.u_log import get_log
    from f_log.color_log import ColorLog
    from f_log.u_decorator import log_func

ULazy.install(globals(), {
    'setup_log': 'f_log.u_log:setup_log',
    'get_log': 'f_log.u_log:get_log',
    'ColorLog': 'f_log.color_log:ColorLog',
    'log_func': 'f_log.u_decorator:log_func',
})
