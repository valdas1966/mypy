from __future__ import annotations
import functools
import inspect
import logging
import os
import re
import time
from datetime import datetime
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

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
# Helpers to extract call info
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


def _format_call_args(func: Callable[..., Any],
                      args: tuple[Any, ...],
                      kwargs: dict[str, Any]) -> str:
    """
    Format arguments as 'name=value' pairs using the function signature.
    """
    try:
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        parts = [f"{name}={value!r}" for name, value in bound.arguments.items()]
        return ", ".join(parts)
    except (TypeError, ValueError):
        return f"args={args!r}, kwargs={kwargs!r}"


# ---------------------------------------------------------------------------
# The decorator
# ---------------------------------------------------------------------------

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """
    Log line format (with colors on console):

      RED   : [ELAPSED_SEC] [dd\\mm\\yyyy hh24:mi:ss]
      YELLOW: CLASS_NAME.FUNC_NAME()
      GREEN : IN[a=..., b=...] OUT[result]

    Example:
      [0] [04\\12\\2025 14:07:32] C.add() IN[a=1, b=2] OUT[3]

    In debug.log the same line appears WITHOUT color codes.
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not DEBUG:
            return func(*args, **kwargs)

        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = int(time.perf_counter() - t0)

        # dd\mm\yyyy hh24:mi:ss
        ts = datetime.now().strftime("%d\\%m\\%Y %H:%M:%S")
        class_name = _get_class_name(func)
        if class_name:
            cf_part = f"{class_name}.{func.__name__}()"
        else:
            cf_part = f"{func.__name__}()"

        arg_str = _format_call_args(func, args, kwargs)

        # Segments
        time_part = f"[{elapsed}] [{ts}]"            # RED
        cf_part_c = cf_part                           # YELLOW
        io_part   = f"IN[{arg_str}] OUT[{result!r}]" # GREEN

        msg = (
            f"{RED}{time_part}{RESET} "
            f"{YELLOW}{cf_part_c}{RESET} "
            f"{GREEN}{io_part}{RESET}"
        )

        logger.debug(msg)
        return result

    return wrapper
