from f_grid.point import Point
from f_grid import u_grid
from f_grid import u_2d
import numpy as np
import random


def get_far_node(grid, src, dist_min, dist_max=float('Infinity')):
    """
    ===========================================================================
     Description:
    ---------------------------------------------------------------------------
        1. Get Grid, Source Node and Distances Boundaries.
        2. Return Random Valid Idd within the Boundaries.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. src : Node
        3. dist_min : int
        4. dist_max : float
    ===========================================================================
     Return: Random and Valid Node Idd (int).
    ===========================================================================
    """
    idds = u_grid.get_valid_idds(grid)
    idds_valid = list()
    for idd in idds:
        dist = u_grid.manhattan_distance(grid, src, idd)
        if (dist >= dist_min) and (dist <= dist_max): 
            idds_valid.append(idd)
    random.shuffle(idds_valid)
    return idds_valid[0]
    
    
def get_nearest(grid, src, dests):
    """
    ===========================================================================
     Description: Return the Nearest Idd to the Src (random if there are many).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. src : int (Node Idd).
        3. dests : set of int (Nodes Idd).
    ===========================================================================
     Return:
    ---------------------------------------------------------------------------
        1. nearest : int (Nearest Node Idd).
        2. distance_nearest : int (Distance from Src to the Nearest Dest).
    ===========================================================================
    """
    nearest = None
    distance_nearest = grid.size
    for dest in dests:
        distance = u_grid.manhattan_distance(grid, src, dest)
        if (distance <= distance_nearest):
            nearest = dest
            distance_nearest = distance
    return nearest, distance_nearest


def get_farthest(grid, src, dests):
    """
    ===========================================================================
     Description: Return the Farthest Idd to the Src (random if there are many).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. src : int (Node Idd).
        3. dests : set of int (Nodes Idd).
    ===========================================================================
     Return:
    ---------------------------------------------------------------------------
        1. nearest : int (Farthest Node Idd).
        2. distance_farthest : int (Distance from Src to the Farthest Dest).
    ===========================================================================
    """
    farthest = None
    distance_farthest = 0
    for dest in dests:
        distance = u_grid.manhattan_distance(grid, src, dest)
        if distance >= distance_farthest:
            farthest = dest
            distance_farthest = distance
    return farthest


def get_total_distances_to(grid, src, dests):
    """
    ===========================================================================
     Description: Return a Total Distances from Source to Destinations.
    ===========================================================================
     Arguments: 
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. src : int (Node Idd).
        3. dests : set of int (Nodes Idds).
    ===========================================================================
     Return: int (Total Distances from Source to Destinations).
    ===========================================================================
    """
    total = 0
    for dest in dests:
        total += u_grid.manhattan_distance(grid, src, dest)
    return total


def get_total_distances_between(grid, idds):
    """
    ===========================================================================
     Description: Return a Total Distances between the Idds.
    ===========================================================================
     Arguments: 
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. idds : set of int (Nodes Idds).
    ===========================================================================
     Return: int (Total Distances between the Idds).
    ===========================================================================
    """
    idds = set(idds)
    total = 0
    for idd in idds:
        total += get_total_distances_to(grid, idd, idds-{idd})
    return total//2


def get_centroid(grid, idds):
    """
    ===========================================================================
     Description: Return Centroid Idd of Set of Idds.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. idds : set of int (Set of Nodes Idds).
    ===========================================================================
     Return:
    ---------------------------------------------------------------------------
        1. int : Centroid.
        2. int : Total Distances from Centroid to Idds.
    ===========================================================================
    """
    centroid = None
    total_min = float('Infinity')
    idds = set(idds)
    for idd in idds:
        total = get_total_distances_to(grid, idd, idds-{idd})
        if (total < total_min):
            centroid = idd
            total_min = total
    return centroid, total_min


def get_centroid_farthest(grid, start, idds):
    """
    ===========================================================================
     Description: Return Centroid Idd of Set of Idds (farhets if many).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. idds : set of int (Set of Nodes Idds).
    ===========================================================================
     Return:
    ---------------------------------------------------------------------------
        1. int : Centroid.
        2. int : Total Distances from Centroid to Idds.
    ===========================================================================
    """
    centroid = None
    total_min = float('Infinity')
    idds = set(idds)
    for idd in idds:
        total = get_total_distances_to(grid, idd, idds-{idd})
        if (total < total_min):
            centroid = idd
            total_min = total
        if (total == total_min):
            if (u_grid.manhattan_distance(grid,start,idd) > u_grid.manhattan_distance(grid,start,centroid)):
                centroid = idd
    return centroid, total_min


def get_shape(grid, idds):
    """
    ===========================================================================
     Description: Return Shape of the Rectangle that Surrounds the Idds.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. idds : set of int (Set of Idds).
    ===========================================================================
     Return:
    ---------------------------------------------------------------------------
        1. int : Amount of Rows in the Rectangle.
        2. int : Amount of Cols in the Rectangle.
    ===========================================================================
    """
    if idds is None: return None
    rows = set()
    cols = set()
    for idd in idds:
        row, col = u_grid.to_row_col(grid, idd)
        rows.add(row)
        cols.add(col)    
    return max(rows)-min(rows)+1, max(cols)-min(cols)+1   


def get_random_idds(grid, idd_center, radius, amount):
    """
    ===========================================================================
     Description: Generate Set of Random Idds in the Rectangle.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. idd_center : int (Idd of Rectangle Center).
        3. radius : int (Radius of Rectangle).
        4. amount : int (Amount of Idds to Random).
    ===========================================================================
     Result:
    ---------------------------------------------------------------------------
        1. set of int (Set of Random Idds in Rectangle).
        2. None if amount of Idds is less then required amount.
    ===========================================================================
    """
    row, col = u_grid.to_row_col(grid, idd_center)
    center = Point(row, col)
    p_min, p_max = u_2d.get_rect(center,radius,radius)
    if not u_grid.is_valid_row_col(grid, p_min.row, p_min.col, by_idd=False):
        return None
    if not u_grid.is_valid_row_col(grid, p_max.row, p_max.col, by_idd=False):
        return None
    grid_sub = grid[p_min.row:p_max.row+1, p_min.col:p_max.col+1]
    idds = []
    for idd in np.nditer(grid_sub):
        if idd >= 0:
            idds.append(int(idd))
    if (idds is None) or (amount > len(idds)):
        return None    
    random.shuffle(idds)
    return set(idds[:amount])


def gen_random_pairs(grid, distance_min, epochs):
    """
    ===========================================================================
     Description: Generate Random Pairs with Epochs where Min Distance.
    ===========================================================================
     Arguments: 
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. distance_min : int (Min Distance between the Pair Idds).
        3. epochs : int (Amount of Attempts).
    ===========================================================================
     Return: set of tuples (int,int) : Random Pairs.
    ===========================================================================
    """
    idds = u_grid.get_valid_idds(grid)
    pairs = set()
    if len(idds)<2:
        return pairs
    for i in range(epochs):
        random.shuffle(idds)
        idd_1 = idds[0]
        idd_2 = idds[1]
        if (u_grid.manhattan_distance(grid, idd_1, idd_2) >= distance_min):
            pairs.add((idd_1,idd_2))
    return pairs
            

"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import sys
   
    def tester_get_far_node():
        grid = u_grid.gen_symmetric_grid(5)
        
        src = 0
        dist_min = 2
        dist_max = 3
        far_nodes = set()
        for i in range(1000):
            far_nodes.add(get_far_node(grid, src, dist_min, dist_max))
        far_nodes_true = {2,3,6,7,10,11,15}
        p1 = far_nodes == far_nodes_true
        
        src = 18
        dist_min = 2
        dist_max = 2
        far_nodes = set()
        for i in range(1000):
            far_nodes.add(get_far_node(grid, src, dist_min, dist_max))
        far_nodes_true = {8,12,14,16,22,24}
        p2 = far_nodes == far_nodes_true
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
        
        
    def tester_get_nearest(): 
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {4,8}
        nearest, distance = get_nearest(grid, start, goals)                     
        
        fname = sys._getframe().f_code.co_name[7:]
        if (nearest == 4 and distance == 2):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
            
            
    def tester_get_farthest(): 
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {4,8}
        farthest, distance = get_farthest(grid, start, goals)                              
        
        fname = sys._getframe().f_code.co_name[7:]
        if (farthest == 8 and distance == 4):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
            
        
    def tester_get_total_distances_to(): 
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {4,8}
        total = get_total_distances_to(grid,start,goals)                            
        
        fname = sys._getframe().f_code.co_name[7:]
        if (total == 6):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
            
            
    def tester_get_total_distances_between(): 
        grid = u_grid.gen_symmetric_grid(3)
        idds = {4,6,8}
        total = get_total_distances_between(grid,idds)                            
        
        fname = sys._getframe().f_code.co_name[7:]
        if (total == 6):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
            
            
    def tester_get_centroid(): 
        grid = u_grid.gen_symmetric_grid(3)
        idds = {2,4,6}
        centroid, total = get_centroid(grid,idds)                            
        
        fname = sys._getframe().f_code.co_name[7:]
        if (centroid == 4 and total == 4):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
            
            
    def tester_get_shape():
        grid = u_grid.gen_symmetric_grid(5)
        idds = {2,4,6}
        shape = get_shape(grid, idds)                           
        
        fname = sys._getframe().f_code.co_name[7:]
        if (shape == (2,4)):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
            
    def tester_get_random_idds():
        grid = u_grid.gen_symmetric_grid(3)
        grid[1][1] = -1
        idds = get_random_idds(grid, idd_center=4, radius=2, amount=2)
        p1 = idds in {frozenset((0,1)),frozenset((0,3)),frozenset((1,3))}
        
        idds = get_random_idds(grid,4,2,4)
        p2 = idds is None
        
        idds = get_random_idds(grid,1,3,2)
        p3 = idds is None
 
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
    
    def tester_gen_random_pairs():
        grid = u_grid.gen_symmetric_grid(3)
        grid[0][0] = -1
        
        pairs = gen_random_pairs(grid, 4, 100)
        f1 = frozenset({(2,6)})
        f2 = frozenset({(6,2)})
        f3 = frozenset({(2,6),(6,2)})
        
        fname = sys._getframe().f_code.co_name[7:]
        if (pairs in {f1,f2,f3}):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
            
    
    
    print('\n====================\nStart Tester\n====================')    
    tester_get_far_node()
    tester_get_nearest()
    tester_get_farthest()    
    tester_get_total_distances_to()
    tester_get_total_distances_between()
    tester_get_centroid()
    tester_get_shape()
    tester_get_random_idds()
    tester_gen_random_pairs()
    print('====================\nEnd Tester\n====================')        
    
    
#tester()
        