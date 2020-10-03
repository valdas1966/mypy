import numpy as np
import u_grid
import queue

def gen_grid_h(grid, goal, lookups=set(), grid_lookup=None):
    """
    ===========================================================================
     Description: Generate Grid of Heuristic values for Idd_1.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Serialized Grid.
        2. goal : int (Node's Id).
        3. lookup : Set of Idds.
        4. grid_lookup : Grid with True Heuristic.
    ===========================================================================
     Return: Grid of Heuristic values for Idd_1.
    ===========================================================================
    """
    grid_h = np.full([grid.shape[0],grid.shape[1]], -1, dtype=int)
    for idd in range(grid.size):
        row, col = u_grid.to_row_col(grid, idd)
        if grid[row][col] >= 0: 
            if idd in lookups:
                grid_h[row][col] = grid_lookup[row][col]
            else:
                grid_h[row][col] = u_grid.manhattan_distance(grid, idd, goal)
    return grid_h


def gen_grid_g(grid, idd):
    """
    ===========================================================================
     Description: Generate Grid of G for Idd.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Serialized Grid.
        2. idd : int (Node's Id).
    ===========================================================================
     Return: Grid of G values for Idd.
    ===========================================================================
    """    
    grid_g = np.full([grid.shape[0],grid.shape[1]], -1, dtype=int)
    g = 0
    closed = set()
    opened = set()
    opened.add(idd)
    while opened:
        opened_temp = opened.copy()
        closed.update(opened_temp)
        opened.clear()
        for cur in opened_temp:
            row, col = u_grid.to_row_col(grid, cur)
            grid_g[row][col] = g
            neighbors = set(u_grid.get_neighbors(grid, row, col))
            opened.update(neighbors - closed)
        g += 1
    return grid_g


def get_expanded_nodes(grid, grid_g, grid_h, goal):
    """
    ===========================================================================
     Description: Return the Number of Expanded Nodes of A* Algorithm.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid_g : Grid of G (of Start).
        2. grid_h : Grid of H (of Goal).
        3. goal : int (Idd number).
    ===========================================================================
     Return: Set of Idds (expanded nodes of A* algorithm).
    ===========================================================================
    """
    grid_f = grid_g + grid_h
    row, col = u_grid.to_row_col(grid_f, goal)
    f = grid_f[row][col]
    grid_f_less = grid * (grid_f < f)
    expanded_nodes = set(np.unique(grid_f_less)) - {-1}
    
    grid_f_equal = grid * (grid_f == f)
    candidate_idds = list(np.unique(grid_f_equal))
    queue_nodes = queue.PriorityQueue()
    for idd in candidate_idds:
        row, col = u_grid.to_row_col(grid, idd)
        queue_nodes.put((-grid_g[row][col],idd))
    idd_cur = queue_nodes.get()
    expanded_nodes.add(idd_cur[1])
    while not queue_nodes.empty():
        idd = queue_nodes.get()
        if u_grid.manhattan_distance(grid, idd_cur[1], idd[1]) == 1:
            expanded_nodes.add(idd[1])
            idd_cur = idd
    
    expanded_nodes.remove(0)                
  
    return expanded_nodes
    
    
    
    
            

"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import sys
    
    def tester_gen_grid_h():
        grid = u_grid.gen_symmetric_grid(3)
        grid[1][2] = -1
        idd_1 = 0
        grid_h = gen_grid_h(grid, idd_1)        
        li_0 = [0,1,2]
        li_1 = [1,2,-1]
        li_2 = [2,3,4]
        lists = [li_0, li_1, li_2]
        grid_h_true = u_grid.lists_to_grid(lists)          
        p1 = (grid_h == grid_h_true).all()
        
        grid = u_grid.gen_symmetric_grid(3)
        grid[1][1] = -1
        grid[2][1] = -1
        goal = 3
        lookup = {1,2,5}
        grid_lookup = np.array([[1,2,3],[0,-1,4],[1,-1,5]], dtype=int)
        grid_h = gen_grid_h(grid, goal, lookup, grid_lookup)
        grid_h_true = np.array([[1,2,3],[0,-1,4],[1,-1,3]], dtype=int)
        p2 = (grid_h == grid_h_true).all()
        
        fname = sys._getframe().f_code.co_name[7:]
        if p1 and p2:        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
            
    def tester_gen_grid_g():
        grid = u_grid.gen_symmetric_grid(3)
        grid[1][1] = -1
        idd_1 = 3
        grid_g = gen_grid_g(grid, idd_1)
        
        li_0 = [ 1, 2, 3]
        li_1 = [ 0,-1, 4]
        li_2 = [ 1, 2, 3]
        lists = [li_0, li_1, li_2]
        grid_g_true = u_grid.lists_to_grid(lists)  
        
        fname = sys._getframe().f_code.co_name[7:]
        if (grid_g == grid_g_true).all():        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
    
    def tester_get_expanded_nodes():
        grid = u_grid.gen_symmetric_grid(5)
        grid[0][0] = -1
        grid[1][1] = -1
        grid[1][2] = -1
        grid[1][4] = -1
        grid[2][1] = -1
        grid[3][1] = -1
        grid[3][2] = -1
        grid[3][4] = -1
        grid_g = np.array([[-1,5,4,3,4],[9,-1,-1,2,-1],[8,-1,0,1,2],[7,-1,-1,2,-1],[6,5,4,3,4]], dtype=int)
        grid_h = np.array([[-1,3,4,5,6],[1,-1,-1,4,-1],[0,-1,2,3,4],[1,-1,-1,4,-1],[2,3,4,5,6]], dtype=int)
        goal = 10
        expanded_nodes = get_expanded_nodes(grid, grid_g, grid_h, goal)
        
        fname = sys._getframe().f_code.co_name[7:]
        if (expanded_nodes == {8,10,12,13,14,15,18,20,21,22,23}):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
               
    
    print('\n====================\nStart Tester\n====================')    
    tester_gen_grid_h() 
    tester_gen_grid_g()
    tester_get_expanded_nodes()
    print('====================\nEnd Tester\n====================')
    
    
#tester()

    
    
    
    
    