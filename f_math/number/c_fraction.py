from f_math.number import u_factor
from f_math.number import u_multiple


class Fraction:

    def __init__(self, numerator, denominator):
        """
        ========================================================================
         Description: Constructs Fraction Number.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. numerator : int
            2. denominator : int
        ========================================================================
        """
        assert type(numerator) == int
        assert type(denominator) == int
        assert numerator >= 0
        assert denominator >= 1
        self.numerator = numerator
        self.denominator = denominator

    def is_proper(self):
        """
        ========================================================================
         Description: Return if the Fraction is Proper.
        ========================================================================
         Return: bool
        ========================================================================
        """
        return self.numerator < self.denominator

    def to_mixed_number(self):
        """
        ========================================================================
         Description: Convert the Fraction into Mixed-Number.
        ========================================================================
         Return: tuple(int, int, int) (Whole Number, Numerator, Denominator)
        ========================================================================
        """
        whole = self.numerator // self.denominator
        numerator = self.numerator % self.denominator
        return whole, numerator, self.denominator

    def simplify(self):
        """
        ========================================================================
         Description: Simplify Fraction (by dividing by GCF(Num,Den).
        ========================================================================
         Return: Fraction (simplified)
        ========================================================================
        """
        gcf = u_factor.gcf(self.numerator, self.denominator)
        numerator = self.numerator // gcf
        denominator = self.denominator // gcf
        return Fraction(numerator, denominator)

    def reciprocal(self):
        """
        ========================================================================
         Description: Return the inverse Fraction.
        ========================================================================
         Return: Fraction (inverse).
        ========================================================================
        """
        return Fraction(numerator=self.denominator, denominator=self.numerator)

    @classmethod
    def from_mixed_number(cls, whole, numerator, denominator):
        """
        ============================================================================
         Description: Convert Mixed-Number into Fraction.
        ============================================================================
         Arguments:
        ----------------------------------------------------------------------------
            1. whole : int
            2. numerator : int
            3. denominator : int
        ============================================================================
         Return: Fraction
        ============================================================================
        """
        assert type(whole) == int
        assert type(numerator) == int
        assert type(denominator) == int
        assert whole >= 0
        assert numerator >= 0
        assert denominator >= 1
        numerator += whole * denominator
        return cls(numerator, denominator)

    @classmethod
    def normalize(cls, f1, f2):
        """
        ========================================================================
         Description: Normalize two Fractions by their LCM
                        (make common denominator).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. f1 : Fraction
            2. f2 : Fraction
        ========================================================================
         Return: tuple(Fraction, Fraction)
        ========================================================================
        """
        assert type(f1) == Fraction
        assert type(f2) == Fraction
        lcm = u_multiple.lcm(f1.denominator, f2.denominator)
        numerator_3 = f1.numerator * (lcm // f1.denominator)
        f3 = Fraction(numerator_3, lcm)
        numerator_4 = f2.numerator * (lcm // f2.denominator)
        f4 = Fraction(numerator_4, lcm)
        return f3, f4

    def __str__(self):
        """
        ========================================================================
         Description: Return Str-Representation of the Fraction in format:
                        Numerator/Denominator
        ========================================================================
         Return: str
        ========================================================================
        """
        return f'{self.numerator}/{self.denominator}'

    def __eq__(self, other):
        """
        ========================================================================
         Description: Return True if the Fraction is equal to other Fraction
                        (numerators and denominators are the same).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. other : Fraction
        ========================================================================
         Return: bool
        ========================================================================
        """
        assert type(other) == Fraction
        return (self.numerator == other.numerator
                and
                self.denominator == other.denominator)

    def __add__(self, other):
        """
        ========================================================================
         Description: Overriding Plus-Operation for Fractions.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. other : Fraction
        ========================================================================
         Return: Simplified Fraction (Result of Plus-Operation).
        ========================================================================
        """
        assert type(other) == Fraction
        f1, f2 = Fraction.normalize(self, other)
        numerator = f1.numerator + f2.numerator
        res = Fraction(numerator, f1.denominator)
        return res.simplify()

    def __sub__(self, other):
        """
        ========================================================================
         Description: Overriding Minus-Operation for Fractions.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. other : Fraction
        ========================================================================
         Return: Simplified Fraction (Result of Minus-Operation).
        ========================================================================
        """
        assert type(other) == Fraction
        f1, f2 = Fraction.normalize(self, other)
        numerator = f1.numerator - f2.numerator
        res = Fraction(numerator, f1.denominator)
        return res.simplify()

    def __mul__(self, other):
        """
        ========================================================================
         Description: Overriding Mult-Operation for Fractions.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. other : Fraction
        ========================================================================
         Return: Simplified Fraction (Result of Mult-Operation).
        ========================================================================
        """
        assert type(other) == Fraction
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        res = Fraction(numerator, denominator)
        return res.simplify()

    def __truediv__(self, other):
        """
        ========================================================================
         Description: Overriding Mult-Operation for Fractions.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. other : Fraction
        ========================================================================
         Return: Simplified Fraction (Result of Mult-Operation).
        ========================================================================
        """
        assert type(other) == Fraction
        return self * other.reciprocal()
