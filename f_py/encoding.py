from f_encoding.base_52 import Base52
from f_utils.dtypes.u_str import UStr as u_str
from f_os.u_folder import UFolder as u_folder
from f_os.u_file import UFile as u_file
from f_file.txt import Txt


class Encoding:
    """
    ============================================================================
     Manages Encoding of Python files.
    ============================================================================
    """

    @staticmethod
    def encode_folder(folder: str, length_to_split=100) -> None:
        """
        ========================================================================
         Encode all Python files in the given folder into CSV based Base52.
        ========================================================================
        """
        paths_py = u_folder.filepaths(folder=folder)
        for path_py in paths_py:
            path_csv = path_py[:-2] + 'csv'
            Encoding.encode(path_py, path_csv, length_to_split)
            u_file.delete(path_py)

    @staticmethod
    def encode(path_py: str,
               path_csv: str,
               length_to_split: int = 100) -> None:
        """
        ========================================================================
         Encode list given Py-File by Base52 and store the result as CSV file.
        ========================================================================
        """
        s_py = str(Txt(path=path_py))
        e_py = Base52.encode(s=s_py)
        lines_py = u_str.split.by_length(s=e_py, length=length_to_split)
        Txt.from_lines(lines=lines_py, path=path_csv)

    @staticmethod
    def decode(path_csv: str,
               path_py: str) -> None:
        """
        ========================================================================
         Decode list given CSV file based on Base52 into an original Py-File.
        ========================================================================
        """
        lines_py = str(Txt(path_csv)).split('\n')
        e_py = ''.join(lines_py)
        d_py = Base52.decode(e=e_py)
        Txt.from_str(s=d_py, path=path_py)
