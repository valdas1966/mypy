import os
import shutil
from distutils.dir_util import copy_tree


def exist(paths):
    """
    ===========================================================================
     Description: True if all Directories in a given List of Paths are exist.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. paths : list of str (List of Full Paths of Directories to Check).
            * If paths is a str of one path, we convert it into a list [path].
    ===========================================================================
     Return: bool (True if all Directories are exist).
    ===========================================================================
    """
    if type(paths) == str:
        paths = [paths]
    ans = True
    for path in paths:
        if not os.path.exists(path):
            ans = False
    return ans
    
 
def delete(paths):
    """
    ===========================================================================
     Description:
    ---------------------------------------------------------------------------
        1. Delete Directories in a List of Paths.
        2. If the Directories are not exist - Pass.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. paths : listt of str (List of Full Paths of Directories to Delete).
            * If paths is a str of one path, we convert it into a list [path].
    ==========================================================================
    """
    if type(paths) == str:
        paths = [paths]
    
    for path in paths:
        if exist(path):
            shutil.rmtree(path) 
        
        
def create(paths):
    """
    ===========================================================================
     Description: Create Directories by a List of Paths (overwrite if exist).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. paths : list of str (List of Full Paths of Directories to Create).
            * If paths is a str of one path, we convert it into a list [path].
    ===========================================================================
    """
    if type(paths) == str:
        paths = [paths]
        
    delete(paths)
    
    for path in paths:
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
        1. path : str (Full Path where to search).
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
         

"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import u_tester
    
    def tester_exist():
        
        path_father = 'c:\\tester_exist'
        path_1 = path_father + '\\1'
        path_2 = path_father + '\\2'
        path_3 = path_father + '\\3' #negative example
        paths = [path_1, path_2]
        create(paths)
        
        p1 = exist(path_1)        
        p2 = exist(paths)        
        p3 = not exist(path_3)
        
        delete(path_father)        
        u_tester.run([p1,p2,p3])
            
            
    def tester_delete():
        
        path_father = 'c:\\tester_delete'
        path_1 = path_father + '\\1'
        path_2 = path_father + '\\2'
        paths = [path_1, path_2]
        create(paths)
        
        delete(path_1)
        p1 = not exist(path_1)
        
        delete(path_father)
        p2 = not exist(path_2)
        
        p3 = not exist(path_father)
        
        u_tester.run([p1,p2,p3])
            
    
    def tester_create():
        
        path_father = 'c:\\tester_create'
        path_1 = path_father + '\\1'
        path_2 = path_father + '\\2'
        paths = [path_1, path_2]
        create(paths)
        
        p1 = exist(paths)
        
        delete(path_father)
        
        u_tester.run(p1)
            
            
    def tester_names_dirs():
        
        path_father = 'c:\\tester_dirs'
        path_1 = path_father + '\\1'
        path_2 = path_father + '\\2'
        paths = [path_1, path_2]
        create(paths)
        
        dirs_test = names_dirs(path_father)
        dirs_true = paths
        
        p1 = dirs_test == dirs_true
        delete(path_father)
        
        u_tester.run(p1)
            
        
    
    print('\n====================\nStart Tester\n====================')    
    tester_exist()
    tester_delete()
    tester_create()
    tester_names_dirs()
    print('====================\nEnd Tester\n====================')        
    
#tester() 