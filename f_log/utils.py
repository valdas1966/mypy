from __future__ import annotations
import functools
import inspect
import logging
import os
import re
import time
from collections.abc import Iterable
from typing import Any, Callable, ParamSpec, TypeVar
from f_psl.datetime import UDateTime
from f_log.color_formatter import ColorFormatter
from f_log.colors import RED, YELLOW, GREEN, RESET, WHITE

P = ParamSpec("P")
R = TypeVar("R")

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
    logger = logging.getLogger(_LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    color_formatter = ColorFormatter("%(message)s")
    strip_color_formatter = StripColorFormatter("%(message)s")

    # Console handler (keeps / adds colors)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    ch.setFormatter(color_formatter)          # <<< here
    logger.addHandler(ch)

    # File handler (colors stripped)
    fh = logging.FileHandler(_LOG_FILE, mode="w", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(strip_color_formatter)
    logger.addHandler(fh)

    return logger



logger = _create_logger()


def set_debug(enabled: bool, path: str = None) -> None:
    """
    Turn debug mode on/off at runtime.
    Call this once from your main() if you want to override the env var.
    """
    global DEBUG
    DEBUG = enabled
    if path:
        global _LOG_FILE
        _LOG_FILE = path

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
    # Summarize only builtin containers as typename(len)
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        if type(value).__module__ == "builtins":
            if hasattr(value, "__len__"):
                try:
                    return f"{type(value).__name__}({len(value)})"
                except Exception:
                    pass

    # For everything else (including GridMap) use repr
    return _short_repr(value, max_len=120)



def _format_call_args(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> list[str]:
    """
    Format arguments as separate '[name=value]' parts using the function
    signature, skipping 'self' and 'cls'.

    Returns:
        list like ['[a=1]', '[b=list(3)]'], where:
          - '[' + 'name=' + ']' will be GREEN (from outer wrapper),
          - the value itself is WHITE.
    """
    try:
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        parts: list[str] = []
        for name, value in bound.arguments.items():
            if name in ("self", "cls"):
                continue
            # key + '=' stay green (outer), value is white, then back to green
            parts.append(
                f"[{name}={WHITE}{_format_value(value)}{GREEN}]"
            )

        return parts

    except (TypeError, ValueError):
        return [
            f"[args={WHITE}{_format_value(args)}{GREEN}]",
            f"[kwargs={WHITE}{_format_value(kwargs)}{GREEN}]",
        ]



def _format_io_lines(arg_parts: list[str], has_output: bool, result: Any) -> list[str]:
    """
    Build IO lines from inputs + optional output.

    Rules (color-aware):
    - inputs + output:
        ['[a=1]', '[b=2] -> <RED>3<GREEN>']
    - inputs only:
        ['[a=1]', '[b=2]']
    - output only:
        ['-> <RED>3<GREEN>']
    - neither:
        []
    """
    inputs = list(arg_parts)
    if has_output:
        raw_output = _format_value(result)
        # Arrow stays green (from outer GREEN), value is RED, then back to GREEN
        colored_output = f"-> {RED}{raw_output}{GREEN}"
    else:
        colored_output = ""

    if inputs and colored_output:
        lines = inputs.copy()
        lines[-1] = f"{lines[-1]} {colored_output}"
        return lines

    if inputs:
        return inputs

    if colored_output:
        return [colored_output]

    return []


def _class_func_name(func: Callable[..., Any]) -> str:
    """Return CLASS.FUNC() or FUNC() if no class."""
    class_name = _get_class_name(func)
    if class_name:
        return f"{class_name}.{func.__name__}()"
    return f"{func.__name__}()"


# ---------------------------------------------------------------------------
# Decorator: log_1 (one line)
# ---------------------------------------------------------------------------

def log_1(func: Callable[P, R]) -> Callable[P, R]:
    """
    Single-call log with multi-line IO if needed.

    Example (2 inputs + output):

      [3] [07/12/2025 09:50:15] to_domain_filepaths() [filepaths=list(25)]
                                                              [extra=list(10) -> 5]

    Colors:
      - time       : RED
      - func name  : YELLOW
      - [key=      : GREEN
      - value      : WHITE
      - output     : RED (after '->')
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not DEBUG:
            return func(*args, **kwargs)

        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = int(time.perf_counter() - t0)

        ts = UDateTime.str_now()
        cf = _class_func_name(func)
        arg_parts = _format_call_args(func, args, kwargs)

        has_output = result is not None
        io_lines = _format_io_lines(arg_parts, has_output, result)

        time_part = f"[{elapsed}] [{ts}]"
        cf_part   = cf

        # Visible, uncolored core prefix (for indent)
        prefix_core = f"{time_part} {cf_part} "
        indent = " " * len(prefix_core)

        if io_lines:
            # First IO line on same line as time + func
            first_io = io_lines[0]
            msg = (
                f"{RED}{time_part}{RESET} "
                f"{YELLOW}{cf_part}{RESET} "
                f"{GREEN}{first_io}{RESET}"
            )
            # Subsequent IO lines, aligned under the first '['
            for extra in io_lines[1:]:
                msg += f"\n{indent}{GREEN}{extra}{RESET}"
        else:
            # No IO part at all
            msg = (
                f"{RED}{time_part}{RESET} "
                f"{YELLOW}{cf_part}{RESET}"
            )

        logger.debug(msg)
        return result

    return wrapper

# ---------------------------------------------------------------------------
# Decorator: log_2 (two lines)
# ---------------------------------------------------------------------------

def log_2(func: Callable[P, R]) -> Callable[P, R]:
    """
    Two-line log per call: start and finish.

    Start (before call):
      [0] [TIMESTAMP] [START] FUNC [a=1]
                                       [b=2]

    Finish (after call):
      [ELAPSED] [TIMESTAMP] [FINISH] FUNC -> RED(3)

    Rules:
    - Start line: inputs only (no output).
    - Finish line: output only (no inputs).
    Colors:
      - time          : RED
      - [START]/[FINISH]: WHITE
      - func name     : YELLOW
      - [key=         : GREEN
      - value         : WHITE
      - output        : RED (after '->')
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not DEBUG:
            return func(*args, **kwargs)

        t0 = time.perf_counter()
        cf = _class_func_name(func)
        arg_parts = _format_call_args(func, args, kwargs)

        # --------------------- Start line --------------------- #
        ts_start = UDateTime.str_now()
        time_part_start = f"[0] [{ts_start}]"

        start_io_lines = _format_io_lines(arg_parts, has_output=False, result=None)

        prefix_core_start = f"{time_part_start} [START] {cf} "
        indent_start = " " * len(prefix_core_start)

        if start_io_lines:
            first_io = start_io_lines[0]
            start_msg = (
                f"{RED}{time_part_start}{RESET} "
                f"{WHITE}[START]{RESET} "
                f"{YELLOW}{cf}{RESET} "
                f"{GREEN}{first_io}{RESET}"
            )
            for extra in start_io_lines[1:]:
                start_msg += f"\n{indent_start}{GREEN}{extra}{RESET}"
        else:
            start_msg = (
                f"{RED}{time_part_start}{RESET} "
                f"{WHITE}[START]{RESET} "
                f"{YELLOW}{cf}{RESET}"
            )

        logger.debug(start_msg)

        # --------------------- Execute function --------------------- #
        result = func(*args, **kwargs)
        elapsed = int(time.perf_counter() - t0)

        # --------------------- Finish line --------------------- #
        ts_end = UDateTime.str_now()
        time_part_end = f"[{elapsed}] [{ts_end}]"

        has_output = result is not None
        finish_io_lines = _format_io_lines([], has_output, result)  # output only

        prefix_core_finish = f"{time_part_end} [FINISH] {cf} "
        indent_finish = " " * len(prefix_core_finish)

        if finish_io_lines:
            first_io = finish_io_lines[0]
            end_msg = (
                f"{RED}{time_part_end}{RESET} "
                f"{WHITE}[FINISH]{RESET} "
                f"{YELLOW}{cf}{RESET} "
                f"{GREEN}{first_io}{RESET}"
            )
            for extra in finish_io_lines[1:]:
                end_msg += f"\n{indent_finish}{GREEN}{extra}{RESET}"
        else:
            end_msg = (
                f"{RED}{time_part_end}{RESET} "
                f"{WHITE}[FINISH]{RESET} "
                f"{YELLOW}{cf}{RESET}"
            )

        logger.debug(end_msg)
        return result

    return wrapper  # <-- IMPORTANT