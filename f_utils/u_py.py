import re
from f_utils import u_dir
from f_utils import u_file
from f_utils import u_filepath


def create_tester_file(filepath: str) -> None:
    dir_file = u_filepath.get_dir(filepath=filepath)
    dir_testers = f'{dir_file}\\testers'
    u_dir.create(dir_testers, overwrite=False)
    filename = u_filepath.get_filename(filepath, with_domain=False)
    class_name = f'Test{snake_to_pascal(snake=filename)}'
    file_tester = f'{dir_testers}\\t_{filename}.py'
    lines = list()
    lines.append('from f_utils import u_tester')
    lines.append('')
    lines.append('')
    lines.append(f'class {class_name}:')
    lines.append('')
    lines.append('    def __init__(self):')
    lines.append('        u_tester.print_start(__file__)')
    lines.append(f'        {class_name}.__tester_()')
    lines.append('        u_tester.print_finish(__file__)')
    lines.append('')
    lines.append('    @staticmethod')
    lines.append('    def __tester_():')
    lines.append('        pass')
    lines.append('')
    lines.append('')
    lines.append("if __name__ == '__main__':")
    lines.append(f'    {class_name}()')
    lines.append('')
    u_file.write_lines(file_tester, lines)


def get_funcs(path):
    """
    ============================================================================
     Description: Return Function Names from Python File.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Path to Python File).
    ============================================================================
     Return: list of str (List of Function Names)
    ============================================================================
    """
    funcs = list()
    file = open(path, 'r')
    for line in file:
        founded = re.findall('\ndef \w*\(', line)
        if len(founded) == 1:
            func = founded[0].strip()
            func = func.replace('def ', '')
            func = func.replace('(', '')
            funcs.append(func)
    file.close()
    return funcs


def change_import(path_dir, old, new, verbose=True):
    """
    ============================================================================
     Description: Change Imports (Modules) in all Python-Files in the Folder.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path_dir : str (Path to Folder with Python-Files).
        2. old : str (Old Module).
        3. new : str (New Module).
        4. verbose : bool (To Print the FilePaths after Update).
    ============================================================================
    """
    filepaths = u_file.filepaths(path_dir, extensions='py')
    for filepath in filepaths:
        u_file.replace_in_file(filepath, [(old, new)])
        if verbose:
            print(filepath)


def snake_to_pascal(snake: str) -> str:
    """
    ============================================================================
     Description: Convert SnakeCase Variable-Name into PascalCase.
    ============================================================================
    """
    pascal = list()
    for i, ch in enumerate(snake):
        if i == 0:
            pascal.append(ch.capitalize())
        elif ch == '_':
            continue
        elif snake[i-1] == '_':
            pascal.append(ch.capitalize())
        else:
            pascal.append(ch)
    return ''.join(pascal)


def is_protected(name: str) -> bool:
    """
    ============================================================================
     Description: Return True if the given Object-Name is protected.
    ============================================================================
    """
    return name.startswith('_') and not '__' in name
