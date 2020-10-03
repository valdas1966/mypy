class Res:
    """
    ===========================================================================
     Description: Class that represents Result of Query.
    ===========================================================================
     Attributes:
    ---------------------------------------------------------------------------
        1. val : The Value of the Result (if is valid).
        2. is_valid : bool (If the Result is valid).
        3. msg : str (Message if the Result is not valid).
    ===========================================================================
    """

    def __init__(self, val=None, is_valid=True):
        """
        =======================================================================
         Description: Constructor - Init Attributes.
        =======================================================================
        """
        self.val = val
        self.is_valid = is_valid
        self.msg = str()
        if not is_valid:
            self.msg = self.val
            self.val = None

    def __bool__(self):
        """
        =======================================================================
         Description: Return True is the Result is valid.
        =======================================================================
         Return: bool (True on valid Result).
        =======================================================================
        """
        return self.is_valid

    def __str__(self):
        """
        =======================================================================
         Description: Return Error Message when Result is invalid.
        =======================================================================
         Return: str (Error Message when Result is invalid or str() otherwise)
        =======================================================================
        """
        return self.msg

    @staticmethod
    def check(res, ora=None):
        if res:
            return
        if ora:
            ora.close()
        print(res.msg)
        exit(1)
