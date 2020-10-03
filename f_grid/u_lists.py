
def to_lists_mask(path, ch_valid):
    """
    ===========================================================================
     Description: Convert File to masked List of Lists [0,-1].
    ---------------------------------------------------------------------------
        1. Init Empty List of Lists.
        2. Open File.
        3. Mask each line to [0,-1] by ch_valid.
        4. Add masked line to List of Lists.
        5. Close the File.
        6. Return the masked List of Lists.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (Path to the File).
        2. ch_valid : str (Valid Char - Mask as 0).
    ===========================================================================
     Return: Masked List of Lists represented by [0,-1].
    ===========================================================================
    """
    lists = []
    
    file = open(path, 'r', encoding='utf-8')
    
    for line in file:        
        lists.append([0 if ch==ch_valid else -1 for ch in line])        
    
    file.close()
    
    return lists

    
def count_rows_cols(lists):
    """
    ===========================================================================
     Description: Count the amount of Rows and Cols of the List of Lists.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. lists : List of Lists.
    ===========================================================================
     Return:
    ---------------------------------------------------------------------------
        1. rows : int (Amount of Rows).
        2. cols : int (Maximum Amount of Cols).
    ===========================================================================
    """
    rows = len(lists)
    cols = max({len(li) for li in lists})
    
    return rows, cols



"""
===============================================================================
===============================================================================
=======           Tester           ============================================
===============================================================================
===============================================================================
"""
import sys

def tester():
    
    def tester_to_lists_mask():
        path = 'C:\\Temp\\temp.map'
        
        file = open(path, 'w')
        file.write('abcde\n')
        file.write('s...\n')
        file.write('g.@.d\n')
        file.close()
        
        lists = to_lists_mask(path, '.')
        
        li_0 = [-1,-1,-1,-1,-1,-1]
        li_1 = [-1,0,0,0,-1]
        li_2 = [-1,0,-1,0,-1,-1]
        lists_true = [li_0, li_1, li_2]
        
        fname = sys._getframe().f_code.co_name[7:]
        if (lists == lists_true):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            

    print('\n====================\nStart Tester\n====================')    
    tester_to_lists_mask()
    print('====================\nEnd Tester\n====================')
    
    
#tester()