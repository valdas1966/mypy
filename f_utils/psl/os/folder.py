from __future__ import annotations
from f_utils.psl.os.u_folder import UFolder
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

    def filepaths(self, recursive: bool = False) -> list[str]:
        """
        ====================================================================
         Get the files of the Folder object.
        ====================================================================
        """
        return UFolder.filepaths(path=self._path, recursive=recursive)

    @staticmethod
    def create(path: str) -> Folder:
        """
        ====================================================================
         Create a Folder object (overwrite if it exists).
        ====================================================================
        """
        if os.path.exists(path):
            Folder.delete(path=path)
        os.makedirs(path)
        return Folder(path=path)
    
    @staticmethod
    def delete(path: str) -> None:
        """
        ====================================================================
         Delete a Folder object even if it is not empty.
        ====================================================================
        """
        shutil.rmtree(path)
