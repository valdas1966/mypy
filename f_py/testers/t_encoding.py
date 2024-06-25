from f_py.encoding import Encoding
from f_os.u_file import UFile as u_file
from f_file.txt import Txt


path_py_in = 'g:\\mypy\\f_py\\encoding.py'
path_py_out = 'g:\\mypy\\f_py\\testers\\temp.py'
path_csv = 'g:\\mypy\\f_py\\testers\\temp.csv'


def test_encode_decode():
    Encoding.encode(path_py_in, path_csv)
    Encoding.decode(path_csv, path_py_out)
    assert str(Txt(path_py_in)) == str(Txt(path_py_out))
    u_file.delete(path_csv)
    u_file.delete(path_py_out)
