from pathlib import Path


def to_path(path: str) -> str:
    """
    ========================================================================
     Convert a local path to full MAC path with home directory.
    ========================================================================
    """
    p = Path.home() / path
    return str(p)
