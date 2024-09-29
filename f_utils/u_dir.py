import os
import shutil
from distutils.dir_util import copy_tree


def is_exist(path: str) -> bool:
    """
    ============================================================================
     Description: Return True if the Dir is exists.
    ============================================================================
    """
    return os.path.exists(path)
    
 
def delete(path: str) -> None:
    """
    ===========================================================================
     Description: Delete Dir in the given Path.
    ===========================================================================
    """
    shutil.rmtree(path)
        
        
def create(path: str, overwrite=False) -> None:
    """
    ============================================================================
     Description: Create Dir in list given Path.
    ============================================================================
    """
    if is_exist(path):
        if overwrite:
            delete(path)
        else:
            return
    os.makedirs(path)


def copy(path_src, path_dest):
    """
    =======================================================================
     Description: Copy Directory from Source-Path into Dest-Path.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path_src : str (Path to the Directory to copy).
        2. path_dest : str (Path where to copy the Directory).
    =======================================================================
    """
    delete(path_dest)
    copy_tree(path_src, path_dest)


def names_dirs(path):
    """
    ===========================================================================
     Description: Return List of Directories' Names in the Path.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. paths : str (Full Path where to search).
    ===========================================================================
     Return: list of str (List of Directories' Names).
    ===========================================================================
    """
    ans = list()
    for name in os.listdir(path):
        full_path = '\\'.join([path,name])
        if os.path.isdir(full_path):
            ans.append(full_path)
    return ans


def get_dir_name(path_dir: str) -> str:
    """
    ============================================================================
     Desc: Return Dir-Name from Dir-Path.
    ============================================================================
     Example:
    ----------------------------------------------------------------------------
                path_dir = 'c:\\nodes\\sub_folder'
                get_dir_name(path_dir) -> 'sub_folder'
    ============================================================================
    """
    return path_dir.split('\\')[-1]
