from collections.abc import UserList
from typing import Generic, TypeVar
import os

T = TypeVar('T')


class FileBase(Generic[T], UserList[T]):
    """
    ============================================================================
     Base-Class for Files.
    ============================================================================
    """

    def __init__(self, path: str) -> None:
        """
        ========================================================================
         Initialize the FileBase object.
        ========================================================================
        """
        self._path = path
        self._lines: list[T] = list()
        # if the file exists, read the lines
        if os.path.exists(path):
            self._read_lines()
        # if the file does not exist, create an empty file
        else:
            open(self._path, 'w').close()

    def write_line(self, line: T) -> None:
        """
        ========================================================================
         Write a line to the file.
        ========================================================================
        """
        self._lines.append(line)

    def save(self) -> None:
        """
        ========================================================================
         Save the lines to the file.
        ========================================================================
        """
        with open(self._path, 'w') as file:
            file.writelines(self._lines)

    def _read_lines(self) -> None:
        """
        ========================================================================
         Read the lines from the file.
        ========================================================================
        """
        with open(self._path, 'r') as file:
            self._lines = file.readlines()
