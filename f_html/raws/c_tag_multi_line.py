class TagMultiLine:
    """
    ===========================================================================
     Description: MultiLine Tag (with opening and closing tag).
    ===========================================================================
     Example: <html>
                 inner
              </html>
    ===========================================================================
     Attributes:
    ---------------------------------------------------------------------------
        1. self.opening : str (The opening tag).
        2. self.inner : str (Inner f_html.raw, empty string as default).
        3. self.closing : str (The closing tag).
    ===========================================================================
    """
    
    def __init__(self, tag, text=str(), indents=0):
        """
        =======================================================================
         Description: Constructor
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. tag : str (Tag Name).
            2. text : str (Text inside the Tag).
            3. indents : int (Number of Indents).
        =======================================================================
        """
        # If there is a text, should be a space between it and the tag name
        if text:
            text = ' {0}'.format(text)
        self.opening = '{0}<{1}{2}>\n'.format('\t'*indents, tag, text)
        self.inner = str()               
        self.closing = '{0}</{1}>\n'.format('\t'*indents, tag)
        
    def add_inner(self, inner):
        """
        =======================================================================
         Description: Add Inner Tag
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. inner : f_html.raw
        =======================================================================
        """
        self.inner += str(inner)

    def __str__(self):
        """
        =======================================================================
         Description: String Representation
        =======================================================================
         Return: str
        =======================================================================
        """
        return '{0}{1}{2}'.format(self.opening, self.inner, self.closing)
    
    def __eq__(self, other):
        """
        =======================================================================
         Description: Equal Operator (if string representations are equal).
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. other : TagMultiLine
        =======================================================================
         Return: bool 
        =======================================================================
        """
        return str(self) == str(other)
    
