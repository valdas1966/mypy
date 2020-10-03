import os
import sys
import shutil
import fileinput
import datetime
from f_utils import u_str
from f_utils import u_set
from f_utils import u_text_mining


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


def write(text, path):
    """
    =======================================================================
     Description: Write text into File.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. text : str (Text to Write).
        2. path : str (Path to File to Write).
    =======================================================================
    """
    file = open(path, 'w')
    file.write(text)
    file.close()


def delete(paths):
    """
    =======================================================================
     Description: Delete a File (by FilePath).
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. paths : str or set of str.
    =======================================================================
    """
    paths = u_set.generalize(paths)
    for path in paths:
        try:
            os.remove(path)
        except:
            print('Cannot Delete: ' + path)


def filepaths(path_dir, extensions=set()):
    """
    =======================================================================
     Description: Return Full-FilePaths of Files in the Directory with
                    the specified extensions (ex: 'txt').
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


def move_file(path_src, path_dest):
    """
    ===========================================================================
     Description: Move file from src to dest.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_src : str (Path to Source File).
        2. path_dest : str (Path where to move the file).
    ===========================================================================
    """
    shutil.copyfile(path_src, path_dest)
    
    
def move_files(path_src, path_dest):
    """
    ===========================================================================
     Description: Move all Files from Source Dir to Destination Dir.
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
        move_file(path_src, path_dest)
    
    
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
            sys.stdout.write(line.replace(what_replace,with_replace))
            
            
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
    str_1 = to_str(path_1)
    str_2 = to_str(path_2)
    return u_text_mining.cosine_similarity(str_1, str_2)


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


"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================

def tester():
    
    import u_tester       
    import u_dir     
        
    def tester_path_to_filename():
        
        path = 'c:\\test\\file.name.py'
        
        # With Domain
        filename_test = path_to_filename(path)
        filename_true = 'file.name.py'
        p1 = filename_test == filename_true
        
        # Without Domain
        filename_test = path_to_filename(path,with_domain=False)
        filename_true = 'file.name'
        p2 = filename_test == filename_true
    
        u_tester.run([p1,p2])
        
    
    def tester_create_txt():
        
        path_dir = 'c:\\tester_create_txt'
        u_dir.create(path_dir)
        
        path_file = path_dir + '\\test.txt'
        
        line_1 = 'hello'
        line_2 = 'world'
        lines = [line_1, line_2]
        create_txt(path_file, lines)
        
        str_test = to_str(path_file)
        str_true = 'hello\nworld\n'
        
        u_dir.delete(path_dir)
        
        p0 = str_test == str_true
        
        u_tester.run([p0])
       
        
        
    def tester_to_str():
        
        path_dir = 'c:\\tester_to_list_words'
        u_dir.create(path_dir)
        
        line_1 = 'aaa\tbbb ccc'
        line_2 = 'ccc bbb aaa'
        lines = [line_1, line_2]
        
        path_file = path_dir + '\\test.txt'
        create_txt(path_file,lines)
        
        str_test = to_str(path_file)
        str_true = 'aaa\tbbb ccc\nccc bbb aaa\n'
        
        p0 = str_test == str_true
        
        u_dir.delete(path_dir)
        
        u_tester.run([p0])


    def tester_cosine_similarity():

        path_dir = 'c:\\tester_cosine_similarity'
        u_dir.create(path_dir)
        
        path_file_1 = path_dir + '\\test_1.txt'
        path_file_2 = path_dir + '\\test_2.txt'
        
        lines = ['hello world']
        create_txt(path_file_1,lines)
        create_txt(path_file_2,lines)
        
        p0 = cosine_similarity(path_file_1, path_file_2) >= 0.99
        
        u_dir.delete(path_dir) 
        
        u_tester.run([p0])
        
        
    def tester_get_paths_by_extension():
    
        path_dir = 'c:\\tester_get_paths_by_extensions'
        u_dir.create(path_dir)
        
        path_dir_1 = path_dir + '\\1'
        path_dir_2 = path_dir + '\\2'
        path_dir_11 = path_dir_1 + '\\11'
        u_dir.create(path_dir_1)
        u_dir.create(path_dir_2)
        u_dir.create(path_dir_11)
                
        path_file_1 = path_dir + '\\test_1.java'
        path_file_2 = path_dir + '\\test_2.java'
        path_file_3 = path_dir_1 + '\\test.java'
        path_file_4 = path_dir_2 + '\\test.java'
        path_file_5 = path_dir_11 + '\\test.java'

        create_txt(path_file_1)
        create_txt(path_file_2)
        create_txt(path_file_3)
        create_txt(path_file_4)
        create_txt(path_file_5)
        
        paths_test = get_paths_by_extension(path_dir, 'java')
        paths_true = [path_file_1, path_file_2, path_file_3, path_file_4, path_file_5] 
        
        u_dir.delete(path_dir)
        
        p0 = set(paths_test) == set(paths_true)
        
        u_tester.run([p0])
        
    
    u_tester.print_start(__file__)
    tester_path_to_filename()
    tester_create_txt()
    tester_to_str()
    tester_cosine_similarity()
    tester_get_paths_by_extension()
    u_tester.print_finish(__file__)        
    
    
#tester()
"""