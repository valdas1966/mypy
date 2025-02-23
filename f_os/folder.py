from __future__ import annotations
import shutil
import os


class Folder:
    """
    ========================================================================
     Folder-Class.
    ========================================================================
    """

    def __init__(self, path: str) -> None:
        """
        ====================================================================
         Initialize the Folder object.
        ====================================================================
        """
        self._path = path   

    @property
    def path(self) -> str:
        """
        ====================================================================
         Get the path of the Folder object.
        ====================================================================
        """
        return self._path

    def files(self) -> list[str]:
        """
        ====================================================================
         Get the files of the Folder object.
        ====================================================================
        """
        return os.listdir(self._path)

    @classmethod
    def create(cls, path: str) -> Folder:
        """
        ====================================================================
         Create a Folder object (overwrite if it exists).
        ====================================================================
        """
        if os.path.exists(path):
            Folder.delete(path=path)
        os.makedirs(path)
        return cls(path=path)
    
    @classmethod
    def delete(cls, path: str) -> None:
        """
        ====================================================================
         Delete a Folder object even if it is not empty.
        ====================================================================
        """
        shutil.rmtree(path)
