from f_file_old.i_1_csv import CSV


class GenCSV:
    """
    ========================================================================
     Generator for CSV files.
    ========================================================================
    """

    @staticmethod
    def abcd(path: str) -> CSV:
        """
        ========================================================================
         Generate a CSV file.
        ========================================================================
        """ 
        titles = ['title_1', 'title_2']
        line_1 = ['a', 'b']
        line_2 = ['c', 'd']
        lines = [line_1, line_2]
        csv = CSV(path=path, titles=titles)
        csv.write_lines(lines=lines)
        return csv
