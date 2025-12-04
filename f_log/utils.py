from __future__ import annotations
import functools
import inspect
import logging
import os
import re
import time
from datetime import datetime
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

# ---------------------------------------------------------------------------
# Colors (ANSI)
# ---------------------------------------------------------------------------

RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RESET  = "\033[0m"

# ---------------------------------------------------------------------------
# Debug flag & logger setup
# ---------------------------------------------------------------------------

DEBUG: bool = os.getenv("DEBUG", "0") == "1"
_LOGGER_NAME = "F_LOG"
_LOG_FILE = "debug.log"


class StripColorFormatter(logging.Formatter):
    """
    Formatter that strips ANSI color codes (for the log file).
    """
    _ansi_re = re.compile(r"\x1b\[[0-9;]*m")

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        return self._ansi_re.sub("", msg)


def _create_logger() -> logging.Logger:
    """
    ========================================================================
     Create Logger.
    ========================================================================
    """
    logger = logging.getLogger(_LOGGER_NAME)

    # Avoid adding handlers twice if this file is imported multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    # We build the whole line ourselves, so only use %(message)s
    plain_formatter = logging.Formatter("%(message)s")
    strip_color_formatter = StripColorFormatter("%(message)s")

    # Console handler (keeps colors)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    ch.setFormatter(plain_formatter)
    logger.addHandler(ch)

    # File handler (colors stripped)
    fh = logging.FileHandler(_LOG_FILE, mode="w", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(strip_color_formatter)
    logger.addHandler(fh)

    return logger


logger = _create_logger()


def set_debug(enabled: bool) -> None:
    """
    Turn debug mode on/off at runtime.
    Call this once from your main() if you want to override the env var.
    """
    global DEBUG
    DEBUG = enabled

    level = logging.DEBUG if DEBUG else logging.INFO
    logger.setLevel(level)

    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setLevel(level)


# ---------------------------------------------------------------------------
# Helpers: names & value formatting
# ---------------------------------------------------------------------------

def _get_class_name(func: Callable[..., Any]) -> str | None:
    """
    Infer class name from function __qualname__.
    Example:
        C.add -> class name 'C'
        add   -> no class (returns None)
    """
    qualname = getattr(func, "__qualname__", "")
    if "." in qualname:
        cls_name, _, _ = qualname.partition(".")
        return cls_name
    return None


def _short_repr(value: Any, max_len: int = 120) -> str:
    """repr(value) truncated to max_len characters."""
    s = repr(value)
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


def _format_value(value: Any) -> str:
    """
    Convert a value to a short, log-friendly string.
    - primitives: normal repr
    - objects with to_log(): use that
    - objects with record(): summarize record
    - collections: summarize
    """
    # Simple primitives
    if isinstance(value, (int, float, bool, type(None))):
        return repr(value)

    if isinstance(value, str):
        return _short_repr(value, max_len=80)

    # Custom log hook: to_log()
    to_log = getattr(value, "to_log", None)
    if callable(to_log):
        try:
            return _short_repr(to_log(), max_len=120)
        except Exception:
            pass

    # HasRecord-style .record()
    rec = getattr(value, "record", None)
    if callable(rec):
        try:
            r = rec()
            cls_name = value.__class__.__name__
            if isinstance(r, dict):
                items = list(r.items())[:3]
                inner = ", ".join(f"{k}={_short_repr(v, 40)}"
                                  for k, v in items)
                return f"{cls_name}({inner}...)"
            return f"{cls_name}({_short_repr(r, 80)})"
        except Exception:
            pass

    # Collections
    if isinstance(value, (list, tuple, set, frozenset)):
        seq = list(value)
        preview = ", ".join(_short_repr(v, 30) for v in seq[:3])
        return f"{type(value).__name__}(len={len(seq)}, [{preview}...])"

    if isinstance(value, dict):
        items = list(value.items())[:3]
        preview = ", ".join(
            f"{_short_repr(k, 20)}={_short_repr(v, 30)}" for k, v in items
        )
        return f"dict(len={len(value)}, {{{preview}...}})"

    # Fallback
    return _short_repr(value, max_len=120)


def _format_call_args(func: Callable[..., Any],
                      args: tuple[Any, ...],
                      kwargs: dict[str, Any]) -> str:
    """
    Format arguments as 'name=value' pairs using the function signature,
    with value rendered by _format_value().
    """
    try:
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        parts = [
            f"{name}={_format_value(value)}"
            for name, value in bound.arguments.items()
        ]
        return ", ".join(parts)
    except (TypeError, ValueError):
        return f"args={_format_value(args)}, kwargs={_format_value(kwargs)}"


def _timestamp_now() -> str:
    """Return timestamp in format dd\\mm\\yyyy hh24:mi:ss."""
    return datetime.now().strftime("%d\\%m\\%Y %H:%M:%S")


def _class_func_name(func: Callable[..., Any]) -> str:
    """Return CLASS.FUNC() or FUNC() if no class."""
    class_name = _get_class_name(func)
    if class_name:
        return f"{class_name}.{func.__name__}()"
    return f"{func.__name__}()"


# ---------------------------------------------------------------------------
# Decorator: one_line
# ---------------------------------------------------------------------------

def one_line(func: Callable[P, R]) -> Callable[P, R]:
    """
    Single-line log per call.

    Format (with colors on console):
      RED   : [ELAPSED] [dd\\mm\\yyyy hh24:mi:ss]
      YELLOW: CLASS.FUNC()
      GREEN : IN[a=..., b=...] OUT[result]

    Example:
      [0] [04\\12\\2025 14:07:32] C.add() IN[a=1, b=2] OUT[3]
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not DEBUG:
            return func(*args, **kwargs)

        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = int(time.perf_counter() - t0)

        ts = _timestamp_now()
        cf = _class_func_name(func)
        arg_str = _format_call_args(func, args, kwargs)

        time_part = f"[{elapsed}] [{ts}]"                       # red
        cf_part   = cf                                          # yellow
        io_part   = f"IN[{arg_str}] OUT[{_format_value(result)}]"  # green

        msg = (
            f"{RED}{time_part}{RESET} "
            f"{YELLOW}{cf_part}{RESET} "
            f"{GREEN}{io_part}{RESET}"
        )
        logger.debug(msg)
        return result

    return wrapper


# ---------------------------------------------------------------------------
# Decorator: two_lines
# ---------------------------------------------------------------------------

def two_lines(func: Callable[P, R]) -> Callable[P, R]:
    """
    Two-line log per call: start and finish.

    Start (before call):
      [0] [dd\\mm\\yyyy hh24:mi:ss] CLASS.FUNC() IN[args...]

    Finish (after call):
      [ELAPSED] [dd\\mm\\yyyy hh24:mi:ss] CLASS.FUNC() OUT[result]
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not DEBUG:
            return func(*args, **kwargs)

        t0 = time.perf_counter()
        cf = _class_func_name(func)
        arg_str = _format_call_args(func, args, kwargs)

        # Start line: elapsed=0, only input
        ts_start = _timestamp_now()
        time_part_start = f"[0] [{ts_start}]"
        start_msg = (
            f"{RED}{time_part_start}{RESET} "
            f"{YELLOW}{cf}{RESET} "
            f"{GREEN}IN[{arg_str}]{RESET}"
        )
        logger.debug(start_msg)

        # Execute function
        result = func(*args, **kwargs)
        elapsed = int(time.perf_counter() - t0)

        # Finish line: real elapsed, only output
        ts_end = _timestamp_now()
        time_part_end = f"[{elapsed}] [{ts_end}]"
        end_msg = (
            f"{RED}{time_part_end}{RESET} "
            f"{YELLOW}{cf}{RESET} "
            f"{GREEN}OUT[{_format_value(result)}]{RESET}"
        )
        logger.debug(end_msg)

        return result

    return wrapper
