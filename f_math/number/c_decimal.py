
class Decimal:

    def __init__(self, dn):
        """
        ========================================================================
         Description: Constructor. Init the attributes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. dn : float
        ========================================================================
        """
        assert type(dn) in {float, int}
        assert dn >= 0
        self.dn = float(dn)

    def decimal_point(self):
        """
        ========================================================================
         Description: Return Index of Decimal Point (from end / right).
        ========================================================================
         Return: int (-1 if not found).
        ========================================================================
        """
        s = str(self.dn)
        i = s.find('.')
        return len(s) - i - 1

    def __eq__(self, other):
        assert type(other) in {Decimal, float}
        if type(other) == Decimal:
            return self.dn == other.dn
        return self.dn == other

    def __add__(self, other):
        assert type(other) == Decimal
        mdp = max(self.decimal_point(), other.decimal_point())
        # shift left the decimal parts (normalize by mdp)
        res = (self.dn * 10**mdp) + (other.dn * 10**mdp)
        # shift right back the decimal parts
        return res / 10**mdp

    def __sub__(self, other):
        assert type(other) == Decimal
        mdp = max(self.decimal_point(), other.decimal_point())
        # shift left the decimal parts (normalize by mdp)
        res = (self.dn * 10**mdp) - (other.dn * 10**mdp)
        # shift right back the decimal parts
        return res / 10**mdp
