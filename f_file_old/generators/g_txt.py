from f_file_old.txt import Txt


class GenTxt:
    """
    ========================================================================
     Generator for Txt objects.
    ========================================================================
    """

    @staticmethod
    def hello_world() -> Txt:
        """
        ====================================================================
         Create a Txt-File with the hello-world message.
        ====================================================================
        """
        lines = ['Hello', 'World']
        path = 'g:\\temp\\hello_world.txt'
        return Txt.create(path=path, lines=lines)
