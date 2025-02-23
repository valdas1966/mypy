from __future__ import annotations
from collections import UserList
import os


class Txt(UserList[str]):
    """
    ========================================================================
     Text-File as List of Strings (Lines).
    ========================================================================
    """

    def __init__(self, path: str) -> None:
        """
        ====================================================================
         Initialize the Txt object (create the file if it does not exist).  
        ====================================================================
        """
        UserList.__init__(self)
        self._path = path
        if not os.path.exists(path):
            open(path, 'w').close()
        lines = open(path, 'r').read().splitlines()
        UserList.__init__(self, lines)

    @property
    def path(self) -> str:
        """
        ====================================================================
         Get the path of the Txt object.
        ====================================================================
        """
        return self._path
    
    @property
    def lines(self) -> list[str]:
        """
        ====================================================================
         Get the lines of the Txt object.
        ====================================================================
        """
        return list(self)
    
    def insert(self, line: str = None, lines: list[str] = None) -> None:
        """
        ====================================================================
         Insert a line or lines into the Txt object.
        ====================================================================
        """
        if line is not None:
            self.append(line)
        elif lines is not None:
            self.extend(lines)
        
    def save(self) -> None:
        """
        ====================================================================
         Save the Txt object to a file with Line-Breaking between Lines.
        ====================================================================
        """
        with open(self._path, 'w') as f:
            for line in self:
                f.write(line + '\n')

    def delete(self) -> None:
        """
        ====================================================================
         Delete the Txt object.
        ====================================================================
        """
        os.remove(self._path)

    def length_line_max(self) -> int:
        """
        ====================================================================
         Return the maximum number of line's length.
        ====================================================================
        """
        return max(len(line) for line in self)

    def __getitem__(self, i: int | slice) -> str | list[str]:
        """
        ====================================================================
         Get an item or a slice from the Txt object.
        ====================================================================
        """
        result = self.data[i]
        # If slicing, return a plain list rather than a new Txt instance.
        if isinstance(i, slice):
            return result
        return result

    @classmethod
    def create(cls, path: str, lines: list[str] = None) -> Txt:
        """
        ====================================================================
         Create a Txt object.
        ====================================================================
        """
        if os.path.exists(path):
            os.remove(path)
        txt = cls(path=path)
        txt.insert(lines=lines if lines else list())
        txt.save()
        return txt
    