from typing import Callable
import shutil
import os


def filepaths(path: str,
              recursive: bool = False,
              predicate: Callable[[str], bool] = None) -> list[str]:
    """
    ========================================================================
     1. Return all filepaths in the given directory path.
     2. Optional boolean argument to include all sub-directories.
     3. Optional predicate function to filter the filepaths.
    ========================================================================
    """
    result = []
    # Scan the directory
    with os.scandir(path) as it:
        # Iterate over the entries (files and directories) in the directory
        for entry in it:
            if entry.is_file():
                # If the entry is a file -> add it to the result
                if not predicate or (predicate and predicate(entry.name)):
                    result.append(entry.path)
            elif entry.is_dir() and recursive:
                # If the entry is a directory and recursive is True ->
                # add all the filepaths in the sub-directory to the result
                result.extend(filepaths(entry.path, recursive, predicate))
    return result


def delete(path: str) -> None:
    """
    ========================================================================
     Delete the directory at the given path.
    ========================================================================
    """
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def create(path: str, name: str) -> None:
    """
    ========================================================================
     Create the directory with the given name at the given path.
    ========================================================================
    """
    delete(f'{path}\\{name}')
    os.makedirs(f'{path}\\{name}')


def is_exist(path: str) -> bool:
    """
    ========================================================================
     Return True if the directory exists at the given path.
    ========================================================================
    """
    return os.path.exists(path)
