import time
import functools
import inspect
from datetime import datetime
from pathlib import Path


_debug_enabled = False
_log_file: Path | None = None


def set_debug(enabled: bool, log_file: str | Path = 'debug.log') -> None:
    """
    Enable or disable debug logging.

    :param enabled: True to enable debug logging
    :param log_file: Path to log file (default: 'debug.log')
    """
    global _debug_enabled, _log_file
    _debug_enabled = enabled
    _log_file = Path(log_file) if enabled else None


def is_debug() -> bool:
    """Return whether debug mode is enabled."""
    return _debug_enabled


def logged(func):
    """
    Decorator that logs function execution details when debug mode is enabled.

    Logs: class_name, func_name, file_path, dt_start, elapsed_ms
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _debug_enabled:
            return func(*args, **kwargs)

        # Get class name (if method)
        class_name = ''
        if args and hasattr(args[0], '__class__'):
            # Check if first arg is 'self' by inspecting the function
            try:
                sig = inspect.signature(func)
                first_param = next(iter(sig.parameters), None)
                if first_param in ('self', 'cls'):
                    class_name = args[0].__class__.__name__
            except (ValueError, TypeError):
                pass

        # Get function name
        func_name = func.__name__

        # Get full file path
        try:
            file_path = inspect.getfile(func)
        except TypeError:
            file_path = '<unknown>'

        # Record start time
        dt_start = datetime.now()
        start_time = time.perf_counter()

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            # Calculate elapsed time in milliseconds
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            # Format log entry
            log_entry = (
                f"{dt_start.isoformat()} | "
                f"{class_name or '-':20} | "
                f"{func_name:30} | "
                f"{file_path} | "
                f"{elapsed_ms:.3f}ms\n"
            )

            # Write to log file
            if _log_file:
                with open(_log_file, 'a') as f:
                    f.write(log_entry)

    return wrapper
