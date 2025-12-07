from __future__ import annotations
import logging
from f_log.colors import WHITE, RESET


class ColorFormatter(logging.Formatter):
    """
    ============================================================================
    Color Formatter.
      - Color INFO messages in white; leave already-colored messages as-is.
    ============================================================================
    """
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)

        # If message already has ANSI codes (your debug logs), don't touch it
        if "\033[" in msg:
            return msg

        # Color INFO messages in white explicitly
        if record.levelno == logging.INFO:
            return f"{WHITE}{msg}{RESET}"

        # Other levels (DEBUG/WARNING/ERROR) without color -> leave default
        return msg
