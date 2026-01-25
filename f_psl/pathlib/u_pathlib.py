import pathlib


def to_mac_path(path: str) -> str:
    """
    ========================================================================
     Convert a local path to full MAC path with home directory.
    ========================================================================
    """
    return str(pathlib.Path.home() / path)


def my_path() -> str:
    """
    ========================================================================
     Get the full path of the caller file.
    ========================================================================
    """
    return str(pathlib.Path(__file__).resolve())


def my_dir() -> str:
    """
    ========================================================================
     Get the directory of the caller file.  ===================================
     ========================================================================
    """
    return str(pathlib.Path(my_path()).parent)
