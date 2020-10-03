
def endswith(text, extensions=set()):
    """
    =======================================================================
     Description: Return True if Text ends with one of the given Extension.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. text : str (Text to Check).
        2. extensions : set of str (Set of Extensions to Check).
    =======================================================================
     Return: bool (True if the Text ends with one of the given Extensions).
    =======================================================================
    """
    if not extensions:
        return True
    for e in extensions:
        if text.endswith(e):
            return True
    return False


def get_nums(text, len_min=1):
    """
    ===========================================================================
     Description: Return List of Numbers that extracted from the str.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. text : str 
    ===========================================================================
     Return: list of int
    ===========================================================================
    """
    nums = list()
    cur = str()
    for ch in text:
        if str.isdecimal(ch):
            if cur:
                cur += ch
            else:
                cur = ch
        else:
            if cur:                
                if len(cur)>=len_min:
                    nums.append(int(cur))    
                cur = str()
    if cur:
        if len(cur)>=len_min:
            nums.append(int(cur))
    return nums


"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import sys
    
    def tester_get_nums(): 
        
        nums = get_nums('1a23bb4')
        p1 = nums == [1,23,4]
        
        nums = get_nums('1a22bb333',3)
        p2 = nums == [333]
              
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))            
    
    print('\n====================\nStart Tester\n====================')    
    tester_get_nums()
    print('====================\nEnd Tester\n====================')        
    
    
#tester()
            