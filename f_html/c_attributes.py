
class Attributes:

    def __init__(self, attributes=dict()):
        """
        ========================================================================
         Description: Constructor. Inits the Attributes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. attributes : dict (ex: {'lang': 'en'})
        ========================================================================
        """
        self.attributes = attributes

    def __str__(self):
        """
        ========================================================================
         Description: Return String-Representation of the Attributes.
        ------------------------------------------------------------------------
         Example: ' weight="30" height="50"'
        ========================================================================
         Return: str
        ========================================================================
        """
        s = str()
        if not self.attributes:
            return s
        for key, value in self.attributes.items():
            if value is None:
                s += ' {0}'.format(key)
            else:
                s += ' {0}="{1}"'.format(key, value)
        return s
