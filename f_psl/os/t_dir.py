from f_psl import u_pathlib
from f_psl.os import u_dir
from f_psl import u_txt


def test_create_delete_is_exist() -> None:
    """
    ========================================================================
     Test the create() method.
    ========================================================================
    """
    # Create a directory in the current working directory
    u_dir.create(path='.', name='dir_test')
    # Get the path of the created directory
    path = str('.\\dir_test')
    # Check if the directory exists
    assert u_dir.is_exist(path=path)
    # Delete the directory
    u_dir.delete(path=path)
    # Check if the directory does not exist
    assert not u_dir.is_exist(path=path)


def test_filepaths() -> None:
    """
    ========================================================================
     Test the filepaths() method.
    ========================================================================
    """
    my_dir = u_pathlib.my_dir()
    # Create a directory in the current working directory
    u_dir.create(path=my_dir, name='dir_test')
    # Create an inner directory in the created directory
    u_dir.create(path=f'{my_dir}\\dir_test', name='dir_test_1')
    # Create a file in the inner directory
    u_txt.from_list(lines=[], path=f'{my_dir}\\dir_test\\dir_test_1\\file.txt')
    # Get the paths of the files in the created directory
    filepaths = u_dir.filepaths(path=f'{my_dir}\\dir_test', recursive=True)
    # Get the true path of the created file
    path_true = f'{my_dir}\\dir_test\\dir_test_1\\file.txt' 
    # Check if the filepaths are correct
    assert filepaths == [path_true]
    # Delete the directory
    u_dir.delete(path=f'{my_dir}\\dir_test')
