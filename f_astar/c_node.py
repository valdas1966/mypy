class Node:
    """
    ===========================================================================
     Decription: Class of Node in Grid.
    ===========================================================================
    """

    def __init__(self, point):
        """
        =======================================================================
         Description: Init Node with Idd.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. point : Point (f_map.c_point).
        =======================================================================
        """
        self.point = point
        self.w = 1  
        self.father = None  
        self.g = float('Infinity')
        self.h = float('Infinity')
        self.f = float('Infinity')

    def __eq__(self, other):
        """
        =======================================================================
         Description: Return True if Self equals to Other.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. other : Node
        =======================================================================
         Return: bool (True if Self equals to Other).
        =======================================================================
        """
        if self.point == other.point:
            return True

    def __ne__(self, other):
        """
        =======================================================================
         Description: Return True if Self not equals to Other.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. other : Node
        =======================================================================
         Return: bool (True if Self not equals to Other).
        =======================================================================
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        =======================================================================
         Description: Return True if Self is less than Other.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. other : Node
        =======================================================================
         Return: bool (True if Self is less than Other).
        =======================================================================
        """
        if self == other:
            return False
        if self.f < other.f:
            return True
        if self.f == other.f:
            if self.g > other.g:
                return True
            elif self.g == other.g and self.point < other.point:
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
        return self == other or self < other

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
        return not (self < other) and not (self == other)

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
        return self == other or self > other

    def __str__(self):
        """
        =======================================================================
         Description: Return String Representation of Node (Node's Point).
        =======================================================================
         Return: str
        =======================================================================
        """
        return str(self.point)
    
    def __repr__(self):
        return str(self.point)

    def __hash__(self):
        """
        =======================================================================
         Description: Return Hash-Value of the Node (Node's Id).
        =======================================================================
         Return: int
        =======================================================================
        """
        return self.idd
    
    
"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import sys
    sys.path.append('D:\\MyPy\\f_utils')
    import u_tester
    
    
    def tester_eq():
        
        node_1 = Node(1)
        node_2 = Node(2)
        node_3 = Node(1)
        
        p0 = node_1 == node_3
        p1 = not (node_1 == node_2)
        
        u_tester.run([p0,p1])
        
        
    def tester_ne():
        
        node_1 = Node(1)
        node_2 = Node(2)
        node_3 = Node(1)
        
        p0 = not (node_1 != node_3)
        p1 = node_1 != node_2
        
        u_tester.run([p0,p1])
        
        
    def tester_lt():
        
        node_1 = Node(1)
        node_2 = Node(2)
        node_3 = Node(3)
        node_1.f = 10
        node_2.f = 20
        node_3.f = 10
        node_1.g = 9
        node_3.g = 1
        
        # equal
        p0 = not (node_1 < node_1)
        
        # f_1 < f_2
        p1 = node_1 < node_2
        
        # f_1 == f_2 and g_1 < g_2
        p2 = node_1 < node_3
        
        u_tester.run([p0,p1,p2])
        
        
    def tester_le():
        
        node_1 = Node(1)
        node_2 = Node(2)
        node_3 = Node(3)
        node_1.f = 10
        node_2.f = 20
        node_3.f = 10
        node_1.g = 9
        node_3.g = 1
        
        # equal
        p0 = node_1 <= node_1
        
        # f_1 < f_2
        p1 = node_1 <= node_2
        
        # f_1 == f_2 and g_1 < g_2
        p2 = node_1 <= node_3
        
        u_tester.run([p0,p1,p2])
        
        
    def tester_gt():
        
        node_1 = Node(1)
        node_2 = Node(2)
        node_3 = Node(3)
        node_1.f = 10
        node_2.f = 20
        node_3.f = 10
        node_1.g = 9
        node_3.g = 1
        
        # equal
        p0 = not (node_1 > node_1)
        
        # f_2 > f_1
        p1 = node_2 > node_1
        
        # f_2 == f_1 and g_2 > g_1
        p2 = node_3 > node_1
        
        u_tester.run([p0,p1,p2])
        
        
    def tester_ge():
        
        node_1 = Node(1)
        node_2 = Node(2)
        node_3 = Node(3)
        node_1.f = 10
        node_2.f = 20
        node_3.f = 10
        node_1.g = 9
        node_3.g = 1
        
        # equal by idd
        p0 = node_1 >= node_1
        
        # f_2 < f_1
        p1 = node_2 >= node_1
        
        # f_1 == f_2 and g_2 > g_1
        p2 = node_3 >= node_1
        
        u_tester.run([p0,p1,p2])
        
        
    def tester_str():
        
        node = Node(1)
        p0 = str(node) == '1'
        
        u_tester.run([p0])
        
        
    def tester_hash():
        
        node = Node(1)
        p0 = hash(node) == 1
        
        u_tester.run([p0])
        
    
    u_tester.print_start(__file__)
    tester_eq()
    tester_ne()
    tester_lt()
    tester_le()
    tester_gt()
    tester_ge()
    tester_str()
    tester_hash()
    u_tester.print_finish(__file__)       
    
    
if __name__ == '__main__':
    tester()
        
  
