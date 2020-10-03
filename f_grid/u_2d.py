from f_grid.point import Point

def get_rect(center, rows, cols):
    """
    ===========================================================================
     Description: Return 2 Points that represents the Rectangle (Min and Max).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. point_center : Point (Center of Rectangle).
        2. rows : int (Radius Rows of Rectangle).
        4. cols : int (Radius Cols of Rectangle).
    ===========================================================================
     Return:
    ---------------------------------------------------------------------------
        1. Point (Min Point of the Rectangle).
        2. Point (Max Point of the Rectangle).
    ===========================================================================
    """
    row_min = center.row - rows//2
    row_max = row_min + rows -1
    col_min = center.col - cols//2
    col_max = col_min + cols - 1
    
    point_min = Point(row_min, col_min)
    point_max = Point(row_max, col_max)
    
    return point_min, point_max


"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import sys
    
    def tester_get_rect():
        center = Point(12,7)
        rows = 4
        cols = 5
        
        p_min, p_max = get_rect(center, rows, cols)
        
        p1 = p_min == Point(10,5)
        p2 = p_max == Point(13,9)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
        
    
    print('\n====================\nStart Tester\n====================')    
    tester_get_rect()
    print('====================\nEnd Tester\n====================')            
    
#tester()
        