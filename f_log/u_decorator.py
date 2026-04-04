import functools
import inspect
import logging
from datetime import datetime
from time import time

from f_log.color_log import ColorLog as cl


def _repr_short(value: object) -> str:
    """
    ========================================================================
     Short repr: collections show type(len), others truncated repr.
    ========================================================================
    """
    if not isinstance(value, str) and hasattr(value, '__len__'):
        return f'{type(value).__name__}({len(value)})'
    text = repr(value)
    if len(text) <= 50:
        return text
    return text[:50] + '...'


def log_func(func):
    """
    ========================================================================
     Decorator that logs func_name, dt_start, args, elapsed, and output.
    ========================================================================
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log = logging.getLogger(func.__module__)
        name = cl.label(func.__name__)
        # Bind args to param names
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        str_args = ', '.join(
            f'{cl.dim(k)}={cl.value(_repr_short(v))}'
            for k, v in bound.arguments.items()
            if k not in ('self', 'cls')
        )
        # Log entry
        dt_start = datetime.now()
        str_dt = cl.time(dt_start.strftime('%d/%m/%Y %H:%M:%S'))
        parts = [name, str_dt]
        if str_args:
            parts.append(str_args)
        log.debug(' | '.join(parts))
        # Execute
        t_start = time()
        try:
            result = func(*args, **kwargs)
            elapsed = time() - t_start
            str_elapsed = cl.time(f'{elapsed:.4f}s')
            str_output = cl.value(_repr_short(result))
            log.debug(f'{name} | {str_elapsed} | -> {str_output}')
            return result
        except Exception as e:
            elapsed = time() - t_start
            str_elapsed = cl.time(f'{elapsed:.4f}s')
            str_error = cl.warn(f'{type(e).__name__}: {e}')
            log.debug(f'{name} | {str_elapsed} | !! {str_error}')
            raise
    return wrapper
