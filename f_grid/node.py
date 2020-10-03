class Node:
    
    def __init__(self, idd):
        """
        =======================================================================
         Description: Init Node with Idd.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. idd : int (Node's Id).
        =======================================================================
        """
        self.idd = idd
        self.w = 1  
        self.g = self.w
        self.father = None  
        self.is_lookup = False       
        self.f = float('Infinity')
        
        
    def generate(self, father=None, h=float('Infinity'), is_lookup=False):
        """
        =======================================================================
         Description: Generate a Node.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. father : Node
        =======================================================================
        """
        self.h = h
        self.is_lookup = is_lookup
        if (father):
            self.father = father
            self.g = father.g + self.w
        self.f = self.g + self.h
            
        
    def update(self, father):
        """
        =======================================================================
         Description: Update Node values if a candidate father is a more
                         optimal than the current father.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. father : Node (Candidate Father).
        =======================================================================
        """
        if self.g > father.g:
            self.father = father
            self.g = father.g + self.w
            self.f = self.g + self.h
        
    
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
        if self.idd == other.idd:
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
        if (self.f < other.f):
            return True
        if (self.f == other.f):
            if (self.is_lookup):
                return True
            if (other.is_lookup):
                return False
            if (self.g >= other.g):
                return True
        return False
    
    
    def __le__(self, other):
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
        return self == other or self > other
    
    
    def __str__(self):
        return str(self.idd)
    
    
    def __hash__(self):
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
    
    def tester_comparision(): 
        # comparision by idd
        node_1 = Node(1)
        node_2 = Node(1)        
        p1 = node_1 == node_2
        
        # comparision by idd
        node_1 = Node(1)
        node_2 = Node(2)
        p2 = node_1 != node_2
        
        # comparision by f
        node_3 = Node(3)
        node_3.generate(h=1)
        node_4 = Node(4)
        node_4.generate(h=2)
        p3 = node_3 < node_4
        
        # comparision by g when f=f
        node_5 = Node(5)
        node_5.generate(father=node_1,h=1)
        p4 = node_5 < node_4        
        
        # comparision by is_lookup when f=f and g=g
        node_6 = Node(6)
        node_6.generate(father=node_1,h=1,is_lookup=True)
        p5 = node_6 < node_5     
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3 and p4 and p5):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))            
    
    print('\n====================\nStart Tester\n====================')    
    tester_comparision()
    print('====================\nEnd Tester\n====================')        
    
    
#tester()
        
  
