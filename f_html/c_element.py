from f_html.c_attributes import Attributes


class Element:

    def __init__(self, tag=None, attributes=dict(),
                 content=str(), is_empty=False):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tag : str (Tag Name).
            2. attributes : dict (Tag Attributes).
            3. content : str (Tag Content).
            4. is_empty : bool (without content and closed tag).
        ========================================================================
         Constraints:
        ------------------------------------------------------------------------
            1. tag or content is not None.
        ========================================================================
        """
        self.tag = tag
        self.attributes = Attributes(attributes)
        self.content = content
        self.is_empty = is_empty
        self.indents = 0
        self.children = list()
        if self.tag and self.content:
            self.nest(Element(content=self.content))

    def nest(self, child):
        """
        ========================================================================
         Description: Nest HTML-Element as list Child.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. child : HTML-Element.
        ========================================================================
        """
        self.is_empty = False
        self.children.append(child)
        child.update_children(self.indents)

    def update_children(self, indents):
        """
        ========================================================================
         Description: Update Children HTML-Elements (increase indents).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
         1. indents : int (Parent Indents).
        ========================================================================
        """
        self.indents = indents + 1
        for child in self.children:
            child.indents = self.indents + 1
            if child.tag:
                child.update_children(self.indents)

    def __str__(self):
        """
        ========================================================================
         Description: Return String-Representation of the HTML Element.
        ========================================================================
         Return: str (ex: '\t<p class="class-name">\n\t\tHello\n\t</p>' )
        ========================================================================
        """
        str_indents = '\t' * self.indents
        if self.tag:
            if self.is_empty:
                s = '{0}<{1}{2}>'
                s = s.format(str_indents, self.tag, str(self.attributes))
            else:
                str_content = '\n'.join([str(child) for child in self.children])
                if str_content:
                    str_content = '\n' + str_content
                s = '{0}<{1}{2}>{3}\n{0}</{1}>'
                s = s.format(str_indents, self.tag, str(self.attributes), str_content)
        # If the Element is Content-Only
        else:
            s = '{0}{1}'.format(str_indents, self.content)
        return s
