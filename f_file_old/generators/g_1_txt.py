from f_file_old.i_1_txt import TXT


class GenTXT:
    """
    ========================================================================
     Generator for TXT files.
    ========================================================================
    """

    @staticmethod
    def abcd(path: str) -> TXT:
        """
        ========================================================================
         Generate a TXT file with two lines.
        ========================================================================
        """
        line_1 = 'ab'
        line_2 = 'cd'
        lines = [line_1, line_2]
        txt = TXT(path=path)
        txt.write_lines(lines=lines)
        return txt
