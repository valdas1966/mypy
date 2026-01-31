from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, replace
from logging.handlers import RotatingFileHandler
from typing import Literal, Optional

Sink = Literal["console", "file", "both"]

@dataclass(frozen=True)
class Settings:
    enabled: bool = True
    level: int = logging.INFO
    sink: Sink = "console"
    path: str = "debug.log"
    max_bytes: int = 5_000_000
    backups: int = 3
    date_fmt: str = "%d/%m/%Y %H:%M:%S"
    console_fmt: str = "[%(levelname)s] [%(asctime)s] %(message)s"
    file_fmt: str = "[%(levelname)s] [%(asctime)s] %(name)s:%(lineno)d %(funcName)s() - %(message)s"

DEFAULTS = Settings()

class NullHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        return

def setup_log(
    *,
    enabled: Optional[bool] = None,
    level: Optional[int] = None,
    sink: Optional[Sink] = None,
    path: Optional[str] = None,
    max_bytes: Optional[int] = None,
    backups: Optional[int] = None,
    console_fmt: Optional[str] = None,
    file_fmt: Optional[str] = None,
    date_fmt: Optional[str] = None,
) -> Settings:
    """
    Configure root logging once at program start.
    Safe to call multiple times (it resets handlers).
    """
    s = replace(
        DEFAULTS,
        enabled=DEFAULTS.enabled if enabled is None else enabled,
        level=DEFAULTS.level if level is None else level,
        sink=DEFAULTS.sink if sink is None else sink,
        path=DEFAULTS.path if path is None else path,
        max_bytes=DEFAULTS.max_bytes if max_bytes is None else max_bytes,
        backups=DEFAULTS.backups if backups is None else backups,
        console_fmt=DEFAULTS.console_fmt if console_fmt is None else console_fmt,
        file_fmt=DEFAULTS.file_fmt if file_fmt is None else file_fmt,
        date_fmt=DEFAULTS.date_fmt if date_fmt is None else date_fmt,
    )

    root = logging.getLogger()

    # Remove existing handlers (avoid duplicates)
    for h in list(root.handlers):
        root.removeHandler(h)

    if not s.enabled:
        root.setLevel(logging.CRITICAL + 1)
        root.addHandler(NullHandler())
        return s

    root.setLevel(s.level)

    if s.sink in ("console", "both"):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(s.level)
        ch.setFormatter(logging.Formatter(s.console_fmt, datefmt=s.date_fmt))
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
