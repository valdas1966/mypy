from pathlib import Path
from f_core.mixins.has.repr import HasRepr


class FileBase(HasRepr):
    """
    ========================================================================
     Base class for file operations.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, path: str) -> None:
        """
        ====================================================================
         Init with a file path. Create empty file if not exists.
        ====================================================================
        """
        self._path = Path(path)
        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.touch()

    @property
    def path(self) -> Path:
        """
        ====================================================================
         Return the file path.
        ====================================================================
        """
        return self._path

    @property
    def name(self) -> str:
        """
        ====================================================================
         Return the file name (with extension).
        ====================================================================
        """
        return self._path.name

    @property
    def stem(self) -> str:
        """
        ====================================================================
         Return the file name (without extension).
        ====================================================================
        """
        return self._path.stem

    @property
    def suffix(self) -> str:
        """
        ====================================================================
         Return the file extension.
        ====================================================================
        """
        return self._path.suffix

    @property
    def size(self) -> int:
        """
        ====================================================================
         Return the file size in bytes.
        ====================================================================
        """
        return self._path.stat().st_size

    def exists(self) -> bool:
        """
        ====================================================================
         Return True if the file exists.
        ====================================================================
        """
        return self._path.exists()

    def delete(self) -> None:
        """
        ====================================================================
         Delete the file. Ignore if not exists.
        ====================================================================
        """
        self._path.unlink(missing_ok=True)

    def __str__(self) -> str:
        """
        ====================================================================
         Return the file path as string.
        ====================================================================
        """
        return str(self._path)
