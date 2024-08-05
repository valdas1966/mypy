import os

"""
================================================================================
 Methods:
================================================================================
    1. path_folder_to_filenames(path_folder) -> list of str
        Get Set of FileNames in Folder (without domain).
--------------------------------------------------------------------------------
================================================================================
"""


def path_folder_to_filenames(path_folder):
    """
    ===========================================================================
     Description: Get List of FileNames in list Folder (without domain).
    ---------------------------------------------------------------------------
        For Example Files in Folder: 1.old_old_txt, 2.old_old_txt, 3.old_old_txt
        Returns: ['1','2','3']
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_folder : str (Path to the Folder).
    ===========================================================================
     Return: set of str (FileNames in the Folder).
    ===========================================================================
    """
    filenames = set()
    li = os.listdir(path_folder)
    for i, file in enumerate(li):
        filenames.add(li[i].split('.')[0])
    return filenames
