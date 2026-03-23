from f_psl.file.i_1_txt.main import FileTxt


class FileTex(FileTxt):
    """
    ========================================================================
     LaTeX file with document structure operations.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def add_document_class(self, name: str) -> None:
        """
        ====================================================================
         Add documentclass command as the first line.
        ====================================================================
        """
        self.write_line(line=f'\\documentclass{{{name}}}',
                        index=0)

    def add_environment(self, name: str) -> None:
        """
        ====================================================================
         Add begin/end environment. Insert before end of document
         if found, otherwise append at end.
        ====================================================================
        """
        begin = f'\\begin{{{name}}}'
        end = f'\\end{{{name}}}'
        ls = self.lines()
        # Find \end{document} to insert before it
        for i, line in enumerate(ls):
            if line.strip() == '\\end{document}':
                ls.insert(i, begin)
                ls.insert(i + 1, end)
                self.text = '\n'.join(ls)
                return
        # No \end{document} found, append at end
        self.write_line(line=begin)
        self.write_line(line=end)
