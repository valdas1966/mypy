from typing import Generic, TypeVar

T = TypeVar('T')


class FileBase(Generic[T]):
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

    def write_lines(self,
                    lines: list[T],
                    append: bool = False) -> None:
        """
        ========================================================================
         Write a list of lines to the file.
        ========================================================================
        """
        lines = [f'{line}\n' for line in lines]
        mode = 'a' if append else 'w'
        with open(self._path, mode) as file:
            file.writelines(lines)

    def read_lines(self, n: int = None) -> list[T]:  
        """
        ========================================================================
         Read the lines from the file.
        ========================================================================
        """
        with open(self._path, 'r') as file:
            if n:   
                lines = [file.readline() for _ in range(n)]
            else:
                lines = file.readlines()
            return [line.strip() for line in lines]
        