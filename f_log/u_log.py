import inspect
import logging
import sys
from dataclasses import dataclass, replace
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Literal

from f_log.color_log import ColorLog

Sink = Literal["console", "file", "both"]


class _ColorFormatter(logging.Formatter):
    """
    ========================================================================
     Formatter that auto-colors log metadata for console output.
    ========================================================================
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        ========================================================================
         Format log record with colored metadata.
        ========================================================================
        """
        msg = super().format(record)
        level = record.levelname
        # Color the [LEVEL] tag
        plain_tag = f'[{level}]'
        colored_tag = ColorLog.dim(f'[') + \
            ColorLog.label(level) + \
            ColorLog.dim(f']')
        msg = msg.replace(plain_tag, colored_tag, 1)
        # Color the [timestamp]
        ts = self.formatTime(record, self.datefmt)
        plain_ts = f'[{ts}]'
        colored_ts = ColorLog.dim(f'[') + \
            ColorLog.time(ts) + \
            ColorLog.dim(f']')
        msg = msg.replace(plain_ts, colored_ts, 1)
        return msg


@dataclass(frozen=True)
class Settings:
    enabled: bool = True
    level: int = logging.INFO
    sink: Sink = "console"
    path: str | None = None
    max_bytes: int = 5_000_000
    backups: int = 3
    date_fmt: str = "%d/%m/%Y %H:%M:%S"
    console_fmt: str = ("[%(levelname)s] [%(asctime)s]"
                        " %(message)s")
    file_fmt: str = ("[%(levelname)s] [%(asctime)s]"
                     " %(name)s:%(lineno)d"
                     " %(funcName)s() - %(message)s")

DEFAULTS = Settings()

def setup_log(
    *,
    enabled: bool | None = None,
    level: int | None = None,
    sink: Sink | None = None,
    path: str | None = None,
    max_bytes: int | None = None,
    backups: int | None = None,
    console_fmt: str | None = None,
    file_fmt: str | None = None,
    date_fmt: str | None = None,
) -> Settings:
    """
    Configure root logging once at program start.
    Safe to call multiple times (it resets handlers).
    """
    overrides = {k: v for k, v in locals().items()
                 if v is not None}
    s = replace(DEFAULTS, **overrides)

    # Auto-generate log path from caller's file and timestamp
    if s.path is None:
        caller = Path(inspect.stack()[1].filename)
        name = caller.stem
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = str(caller.parent / f'{name}_{ts}.log')
        s = replace(s, path=path)

    root = logging.getLogger()

    # Remove existing handlers (avoid duplicates)
    for h in list(root.handlers):
        root.removeHandler(h)

    if not s.enabled:
        root.setLevel(logging.CRITICAL + 1)
        root.addHandler(logging.NullHandler())
        return s

    root.setLevel(s.level)

    if s.sink in ("console", "both"):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(s.level)
        ch.setFormatter(_ColorFormatter(s.console_fmt,
                                        datefmt=s.date_fmt))
        root.addHandler(ch)

    if s.sink in ("file", "both"):
        fh = RotatingFileHandler(
            s.path,
            maxBytes=s.max_bytes,
            backupCount=s.backups,
            encoding="utf-8",
        )
        fh.setLevel(s.level)
        fh.setFormatter(logging.Formatter(s.file_fmt, datefmt=s.date_fmt))
        root.addHandler(fh)

    return s


def get_log(name: str) -> logging.Logger:
    """
    ========================================================================
     Return a Logger for the given module name.
    ========================================================================
    """
    return logging.getLogger(name)
