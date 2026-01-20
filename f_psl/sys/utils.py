import sys


def is_mac() -> bool:
    """
    ========================================================================
     Return True if the system is macOS.
    ========================================================================
    """
    return sys.platform == 'darwin'