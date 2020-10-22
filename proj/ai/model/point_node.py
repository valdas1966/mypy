from proj.ai.model.point import Point


class Node(Point):
    """
    ===========================================================================
     Description: Class of Node in the Map.
    ===========================================================================
    """

    def __init__(self, point=None, x=None, y=None, goal=None):
        """
        =======================================================================
         Description: Init Node with Idd.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. point : Point.
            2. x : int.
            3. y : int.
            4. goal : Point (for heuristic calculation).
        =======================================================================
        """
        if point:
            x, y = point.x, point.y
        super().__init__(x, y)
        self.father = None
        self.w = 1
        self.g = 0
        self.h = float('Infinity')
        self.__set_h(goal)
        self.__set_f()

    def update(self, father_cand, goal):
        """
        =======================================================================
         Description: Update Node (Father and G).
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. father_cand : Node
            2. goal : Point
        =======================================================================
        """
        self.__set_father(father_cand)
        self.__set_h(goal)
        self.__set_f()

    def __set_father(self, father_cand):
        """
        ========================================================================
         Description: Set Candidate-Father if it is better from the current.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. father_cand : Node
        ========================================================================
        """
        # calculate a candidate g
        g_cand = father_cand.g + self.w
        # if does not have father or the candidate father is better
        if not self.father or self.g > g_cand:
            # set the candidate father as father
            self.father = father_cand
            self.g = g_cand

    def __set_h(self, goal):
        """
        ========================================================================
         Description: Set Heuristic to the Goal (Infinity if there is no Goal).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. goal : Point
        ========================================================================
        """
        if goal and self.h == float('Infinity'):
            self.h = self.distance(goal)

    def __set_f(self):
        """
        ========================================================================
         Description: Set Cost-Function (F = G + H).
        ========================================================================
        """
        self.f = self.g + self.h

    def __lt__(self, other):
        """
        =======================================================================
         Description: Return True if Self is less than other Node.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. other : Node
        =======================================================================
         Return: bool (True if Self is less than other Node).
        =======================================================================
        """
        if self == other:
            return False
        if self.f < other.f:
            return True
        if self.f == other.f:
            if self.g > other.g:
                return True
            elif self.g == other.g:
                if Point(self.x, self.y) < Point(other.x, other.y):
                    return True
        return False

    def __le__(self, other):
        """
        =======================================================================
         Description: Return True if Self is less or equal to Other.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. other : Node
        =======================================================================
         Return: bool
        =======================================================================
        """
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        """
        =======================================================================
         Description: Return True if Self is greater than Other.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. other : Node
        =======================================================================
         Return: bool (True if Self is greater than Other).
        =======================================================================
        """
        return not self.__le__(other)

    def __ge__(self, other):
        """
        =======================================================================
         Description: Return True if Self is greater or equal than Other.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. other : Node
        =======================================================================
         Return: bool
        =======================================================================
        """
        return not self.__lt__(other)
