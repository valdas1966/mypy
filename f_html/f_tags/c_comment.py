import sys
sys.path.append('D:\\MyPy')

from f_html.c_element import Element

class TagComment:

    def __init__(self, comment):
        """
        ========================================================================
         Description: Constructor. Inits the Attributes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. comment : str (The Comment itself).
        ========================================================================
        """
        comment = '!-- {0} --'.format(comment)
        self.tag = Element(tag=comment)

    def __str__(self):
        """
        ========================================================================
         Description: Return string-representation of the Comment Tag.
        ------------------------------------------------------------------------
            1. Example: <!-- comment -->
        ========================================================================
        """
        return str(self.tag)
