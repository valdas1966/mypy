from __future__ import annotations
from typing import Iterator
from f_abstract.mixins.nameable import Nameable
from f_utils.dtypes.u_list import UList
from f_utils.dtypes.u_str import UStr


class Txt(Nameable):
    """
    ============================================================================
     Text-File Manager.
    ============================================================================
    """

    def __init__(self, path: str) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=path)

    @classmethod
    def from_str(cls,
                 s: str,
                 path: str) -> Txt:
        """
        ========================================================================
         Generate Txt-File from a given String.
        ========================================================================
        """
        with open(file=path, mode='w') as file:
            file.write(s)
        return Txt(path=path)

    @classmethod
    def from_lines(cls,
                   lines: list[str],
                   path: str) -> Txt:
        """
        ========================================================================
         Generate Txt-File from a given List of Lines.
        ========================================================================
        """
        lines = Txt.add_end_lines(lines)
        with open(file=path, mode='w') as file:
            file.writelines(lines)
        return Txt(path=path)

    @classmethod
    def add_end_lines(cls, li: list[str]) -> list[str]:
        """
        ========================================================================
         Add End-Line char to every Line (except the Last).
        ========================================================================
        """
        return UList.apply.except_last(li, func=UStr.add.end_line)

    @property
    def path(self) -> str:
        return self._name

    def add_line(self, line: str, index: int = None) -> None:
        """
        ========================================================================
         Add a Line at a specified Index in the File.
        ========================================================================
        """
        lines = list(self)
        if index is None:
            lines.append(line)
        else:
            lines.insert(index, line)
        lines = UList.apply.except_last(lines, func=lambda x: f'{x}\n')
        with open(self._name, 'w') as file:
            file.writelines(lines)

    def __str__(self) -> str:
        """
        ========================================================================
         Return Text-File as String.
        ========================================================================
        """
        with open(self._name, 'r') as file:
            return file.read()

    def __repr__(self) -> str:
        """
        ========================================================================
         Return an informative Object Representation.
         Ex: <Txt: Path>
        ========================================================================
        """
        return f'<{type(self).__name__}: {self.path}>'

    def __iter__(self) -> Iterator:
        """
        ========================================================================
         Return Text-File as List of Lines (without End-Line chars).
        ========================================================================
        """
        with open(self._name, 'r') as file:
            return iter([line.rstrip('\n') for line in file])
