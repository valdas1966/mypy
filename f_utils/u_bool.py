def all(predicates):
    """
    ===========================================================================
     Description: Return True if all Predicates are True.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. predicates : list of bool (List of Predicates).
    ===========================================================================
     Return: bool (True if all Predicates are True).
    ===========================================================================
    """
    if type(predicates) == bool:
        predicates = [predicates]
    for p in predicates:
        if not p:
            return False
    return True


def first_false(predicates):
    """
    ===========================================================================
     Description: Return the index of first false predicate (None if all True).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. predicates : list of bool (List of Predicates).
    ===========================================================================
     Return: int (Index of First False Predicate. None if all are True).
    ===========================================================================
    """
    for i, p in enumerate(predicates):
        if not p:
            return i
    return None

"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
   
    def tester_all():
        predicates = [True, True, True]
        p1 = all(predicates)
        
        predicates = [True,False,True]
        p2 = not all(predicates)
        
        predicates = [False,False,False]
        p3 = not all(predicates)
        
        predicates = True
        p4 = all(predicates)
        
        if (p1 and p2 and p3 and p4):
            print('OK: all')
        else:
            print('Failed: all')
            
            
    def tester_first_false():
        
        # All are False
        predicates = [False, False]
        p0 = first_false(predicates) == 0
        
        # All are True
        predicates = [True, True]
        p1 = first_false(predicates) == None

        # First is False
        predicates = [False, True]
        p2 = first_false(predicates) == 0
        
        # Last is False
        predicates = [True, False]
        p3 = first_false(predicates) == 1
        
        if (p0 and p1 and p2 and p3):
            print('OK: first_false')
        else:
            print('Failed: first_false')
            
    
    print('\n====================\nStart Tester\n====================')    
    tester_all()
    tester_first_false()
    print('====================\nEnd Tester\n====================')            
    
#tester()
        
    
    