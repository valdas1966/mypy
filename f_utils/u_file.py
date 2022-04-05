import os
import sys
import shutil
import fileinput
import datetime
from f_utils import u_str
from f_utils import u_set


def is_exists(path):
    """
    ============================================================================
     Description: Return True if the file is exist.
    ============================================================================
     Arguemtns:
    ----------------------------------------------------------------------------
        1. path : str (Path to the File).
    ============================================================================
    """
    return os.path.isfile(path)


def read(path):
    """
    =======================================================================
     Description: Return the file as string.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path : str (Path to File for reading).
    =======================================================================
     Return: str (String-Representation of the File).
    =======================================================================
    """
    file = open(path, 'r')
    text = file.read()
    file.close()
    return text


def write(path, text):
    """
    =======================================================================
     Description: Write text into File.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path : str (Path to File to Write).
        2. text : str (Text to Write).
    =======================================================================
    """
    file = open(path, 'w')
    file.write(text)
    file.close()


def append(path, text):
    """
        =======================================================================
         Description: Write text into File.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. path : str (Path to File to Append).
            2. text : str (Text to Append).
        ========================================================================
        """
    file = open(path, 'a')
    file.write(text)
    file.close()


def delete(paths, verbose=True):
    """
    =======================================================================
     Description: Delete a File (by FilePath).
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. paths : str or set of str.
        2. verbose : bool (to print the error msg or not).
    =======================================================================
    """
    paths = u_set.generalize(paths)
    for path in paths:
        try:
            os.remove(path)
        except Exception as e:
            if verbose:
                print('Cannot Delete: ' + path + '\n' + str(e))


def to_list(path, verbose=False):
    """"
    ============================================================================
     Description: Transpose Elements from Text-File into a List.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Path to Text-File).
        2. verbose : bool
    ============================================================================
     Return: list of str
    ============================================================================
    """
    text = read(path)
    if verbose:
        cnt = text.count('\n')+1
        print(f'{cnt} elements are inserted into a list from {path}')
    return text.split('\n')


def to_set(path, verbose=False):
    """"
    ============================================================================
     Description: Transpose Elements from Text-File into a Set.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Path to Text-File).
        2. verbose : bool
    ============================================================================
     Return: set of str
    ============================================================================
    """
    li = to_list(path, verbose)
    s = set(li)
    if verbose:
        print(f'{len(s)} elements are inserted into a set from {path}')
    return s


def filepaths(path_dir, extensions=set()):
    """
    =======================================================================
     Description: Return Full-FilePaths of Files in the Directory with
                    the specified extensions (ex: 'txt').
                  If extensions is empty -> Return all FilePaths.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path_dir : str (Path to Directory to Inspect).
        2. extensions : str or set (str if one extensions, set if many).
                        The extensions should be like: 'txt', 'py' and etc.
    =======================================================================
     Return: list of str (List of Full-FilePaths).
    =======================================================================
    """
    extensions = u_set.generalize(extensions)
    extensions = {'.' + e for e in extensions}
    li = list()
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            if u_str.endswith(file, extensions):
                filepath = os.path.join(root, file)
                li.append(filepath)
    return li


def get_files_names(path):
    """
    ===========================================================================
     Description: Return List of Files Names in the Path.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (Path where to search).
    ===========================================================================
     Return: list of str (List of Files Names).
    ===========================================================================
    """
    names = list()
    for name in os.listdir(path):
        full_path = path + '\\' + name
        if os.path.isfile(full_path):
            names.append(name)
    return names


def copy(path_src, path_dest):
    """
    ===========================================================================
     Description: Copy file from src to dest.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_src : str (Path to Source File).
        2. path_dest : str (Path where to move the file).
    ===========================================================================
    """
    shutil.copyfile(path_src, path_dest)
    
    
def copy_files(path_src, path_dest):
    """
    ===========================================================================
     Description: Copy all Files from Source Dir to Destination Dir.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_src : str (Path to Source Directory).
        2. path_dest : str (Path to Destination Directory).
    ===========================================================================
    """
    names = get_files_names(path_src)
    for name in names:
        path_src = u_str.get_path(path_src,name)
        path_dest = u_str.get_path(path_dest,name)
        copy(path_src, path_dest)
    
    
def replace_in_file(path, tuples):
    """
    ===========================================================================
     Description: Replace string in File.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path  : str (Path of File to change).
        2. tuples : list of tuples (Every Tuple contains what_replace and
                        with_replace, e.g ('a','o')).
    ===========================================================================
    """
    for t in tuples:
        what_replace = t[0]
        with_replace = t[1]
        for line in fileinput.input(path, inplace=1):                    
            sys.stdout.write(line.replace(what_replace, with_replace))
            
            
def get_filename(path, with_domain=True):
    """
    ===========================================================================
     Description: Extract FileName from the Path (with or without domain).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (FullPath of the FileName).
        2. with_domain : bool (Domain is for example .txt or .py).
    ===========================================================================
     Return: str (FileName extracted from the FullPath).
    ===========================================================================
    """  
    vals = path.split('\\')
    filename = vals[-1]
    if not with_domain:
        vals = filename.split('.')
        filename = '.'.join(vals[:-1])
    return filename

    
def create_txt(path, lines=list()):
    """
    ===========================================================================
     Description: Create Text File from List of Lines (str + '\n').
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (Path to Text File to create).
        2. lines : list of str (List of Lines str + '\n').
    ===========================================================================
    """
    file = open(path, 'w')
    for line in lines:
        file.write(line + '\n')
    file.close()


def cosine_similarity(path_1, path_2):
    """
    ===========================================================================
     Description: Return Cosine Similarity between two text files.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_1 : str (Path to the first File).
        2. path_2 : str (Path to the second File).
    ===========================================================================
     Return: float (Cosine Similarity between the two files).
    ===========================================================================
    """
    # str_1 = to_str(path_1)
    # str_2 = to_str(path_2)
    # return u_text_mining.cosine_similarity(str_1, str_2)
    pass


def datetime_created(filepath):
    """
    ============================================================================
     Description: Return DateTime when the File was Created.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. filepath : str (Path to the File).
    ============================================================================
     Return: DateTime.
    ============================================================================
    """
    t = os.path.getctime(filepath)
    return datetime.datetime.fromtimestamp(t)


def replace_filename(path, filename):
    """
    ============================================================================
     Description: Get full filepath and return it with replaced filename.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Full FilePath).
        2. filename : str (FileName to Replace).
    ============================================================================
     Return: str (FilePath with replaced FileName).
    ============================================================================
    """
    return '\\'.join(path.split('\\')[:-1]) + '\\' + filename
