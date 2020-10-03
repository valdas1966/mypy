import random
import numpy as np
import collections
import math
from f_grid import u_lists


def gen_dict_weights(n):
    """
    ===========================================================================
     Description: Return Dictionary of random weights between 1 and n.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. n : int (Size of the Dict and Maximum Range of Weight).
    ===========================================================================
    """
    dict_w = dict()
    for i in range(n):
        dict_w[i] = random.randint(1,n)
    return dict_w
    

def get_center(grid):
    """
    ===========================================================================
     Description: Return Idd of Grid's Center.
    ===========================================================================
     Arguments: 
    ---------------------------------------------------------------------------
        1. grid : Serialized Grid.
    ===========================================================================
     Return: Idd : int (Center Node's Id).
    ===========================================================================
    """
    row = math.floor(grid.shape[0] / 2)
    col = math.floor(grid.shape[1] / 2)
    idd = to_idd(grid, row, col)
    x = 0
    while (idd == -1):
        x += 1
        idd = to_idd(grid, row-x, col-x)
        if (idd >= 0): break
        idd = to_idd(grid, row-x, col)
        if (idd >= 0): break
        idd = to_idd(grid, row-x, col+x)
        if (idd >= 0): break
        idd = to_idd(grid, row, col-x)
        if (idd >= 0): break
        idd = to_idd(grid, row, col+x)
        if (idd >= 0): break
        idd = to_idd(grid, row+x, col-x)
        if (idd >= 0): break
        idd = to_idd(grid, row+x, col)
        if (idd >= 0): break
        idd = to_idd(grid, row+x, col+x)           
    return idd
    
    
def lists_to_grid(lists):
    """
    ===========================================================================
     Description: Convert List of Lists to Binary Grid.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. lists : List of Lists
    ===========================================================================
     Return: Binary Grid - 2D Arranged Numpy Array of [0,-1] 
    ===========================================================================
    """
    rows, cols = u_lists.count_rows_cols(lists)    
    
    grid = np.full(shape=[rows,cols], fill_value=-1, dtype=int)

    for row in range(rows):
        for col in range(len(lists[row])):
            grid[row][col] = lists[row][col]
        
    return grid


def to_row_col(grid, idd):
    """
    ===========================================================================
     Description: Return Row and Col indexes of the Idd.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : 2D Serialized Numpy Array.
        2. idd : int (Node's Id).
    ===========================================================================
     Return: row, col : int, int
    ===========================================================================
    """
    row = idd // grid.shape[1]
    col = idd % grid.shape[1]
    return row, col


def to_idd(grid, row, col):
    """
    ===========================================================================
     Description: Return Node's Id by Row and Col combination.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : 2D Serialized Numpy Array.
        2. row : int
        3. col : int
    ===========================================================================
     Return: idd : int (Node's Id).
    ===========================================================================
    """
    if is_valid_row_col(grid, row, col):
        return row*grid.shape[1] + col
    else:
        return -1


def is_valid_row_col(grid, row, col, by_idd=True):
    """
    ===========================================================================
     Description: Return True if Row and Col are in the Shapes of Grid.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. row : int
        3. col : int
        4. by_idd : bool 
    ===========================================================================
     Return: True if Row and Col are in the Shapes of Grid.
    ===========================================================================
    """
    if (row<0) or (col<0) or (row>=grid.shape[0]) or (col>=grid.shape[1]):
        return False
    if (by_idd and (grid[row][col] == -1)):
        return False
    return True


def is_valid_idd(grid, idd):
    """
    ===========================================================================
     Description: Return True if Idd is valid.
    ---------------------------------------------------------------------------
     Validation is by:
         1. Location in the Shapes of the Grid.
         2. Positive Idd in the Grid.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. idd : int (Node's Id)
    ===========================================================================
     Return: True if Idd is valid.
    ===========================================================================
    """
    row, col = to_row_col(grid, idd)
    return is_valid_row_col(grid, row, col)


def get_valid_idds(grid):
    """
    ===========================================================================
     Description: Return List of Valid Idd in the Grid.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
    ===========================================================================
     Return: List of Valid Idd (int).
    ===========================================================================
    """
    valid_idds = []
    for idd in np.nditer(grid):
        if is_valid_idd(grid, idd):
            valid_idds.append(int(idd))
    return valid_idds            
    
    
def get_neighbors(grid, row=None, col=None, idd=None):
    """
    ===========================================================================
     Description: Return List of Valid Neighbors (int).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Numpy 2D Array.
        2. row : int
        3. col : int
    ===========================================================================
     Return: List of Valid Neighbors (list of int).
    ===========================================================================
    """
    if not idd == None:
        row, col = to_row_col(grid, idd)
        
    def add_neighbor(row, col):
        idd = to_idd(grid, row, col)
        if grid[row][col] >= 0:
            neighbors.append(idd)
        
    neighbors = list()
    
    if (row > 0):
        add_neighbor(row-1, col)
    if (col < grid.shape[1]-1):
        add_neighbor(row, col+1)
    if (row < grid.shape[0]-1):
        add_neighbor(row+1, col)
    if (col > 0):
        add_neighbor(row, col-1)
    
    return neighbors        


def to_course(grid, idd_1, idd_2):
    """
    ===========================================================================
     Description: Return the course from Idd_1 to Idd_2.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Canonized Grid.
        2. idd_1 : int (Node's Id).
        3. idd_2 : int (Node's Id).
    ===========================================================================
     Return: str (Course) {'UP','RIGHT','DOWN','LEFT'}
    ===========================================================================
    """
    row_1, col_1 = to_row_col(grid, idd_1)
    row_2, col_2 = to_row_col(grid, idd_2)
        
    if (col_1 == col_2):
        if (row_1 == row_2+1):
            return 'UP'
        if (row_1 == row_2-1):
            return 'DOWN'
    elif (row_1 == row_2):
        if (col_1 == col_2+1):
            return 'LEFT'
        if (col_1 == col_2-1):
            return 'RIGHT'        
    return 'ERROR'
        

def to_next_idd(grid, idd, course):
    """
    ===========================================================================
     Description: Return the Idd of the Next Node (by Course).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid.
        2. idd : int (Node's Id).
        3. course : str {'UP','RIGHT','DOWN','LEFT'}.
    ===========================================================================
     Return: int (Next Node's Id).
    ===========================================================================
    """
    row, col = to_row_col(grid, idd)
    if course == 'UP':
        row -= 1
    elif course == 'DOWN':
        row += 1
    elif course == 'LEFT':
        col -= 1
    elif course == 'RIGHT':
        col += 1
    else:
        return -1
    return to_idd(grid, row, col)    
        

def remove_deadlocks(grid):
    """
    ===========================================================================
     Description: Remove Deadlocks from the Grid (Nodes without Neighbors).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid with [-1] as Block.
    ===========================================================================
     Return: 2D Binary Numpy Array without Deadlocks.
    ===========================================================================
    """
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row][col] >= 0:
                if not get_neighbors(grid, row, col):
                    grid[row][col] = -1
    return grid
    

def remove_empty_rows(grid):
    """
    ===========================================================================
     Desription: Remove Empty Rows from Grid (Empty = -1).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid to be changed.
    ===========================================================================
    """
    return grid[~np.all(grid == -1, axis=1)]   
    
    
def remove_empty_cols(grid):
    """
    ===========================================================================
     Desription: Remove Empty Cols from Grid (Empty = -1).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid to be changed.
    ===========================================================================
    """
    grid = grid.transpose()
    grid = remove_empty_rows(grid)
    return grid.transpose()
    
    
def serialize(grid):
    """
    ===========================================================================
     Description: Convert Grid [with -1] to Serialized Grid [0,1,-1,3].
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid with [-1] as Block.
    ===========================================================================
     Return: Serialized Numpy 2D Array.
    ===========================================================================
    """
    counter = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row][col] >= 0:
                grid[row][col] = counter
            else:
                grid[row][col] = -1
            counter += 1
    return grid


def canonize(grid):
    """
    ===========================================================================
     Description: Canonize Binary Grid [0,1] to Serialized [0,1,2,-1,4].
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Binary Grid [0,1].
    ===========================================================================
     Return: Canonized 2D Grid.
    ===========================================================================
    """
    grid = remove_deadlocks(grid)
    grid = remove_empty_rows(grid)
    grid = remove_empty_cols(grid)
    return serialize(grid)


def xor(grid_1, grid_2):
    """
    ===========================================================================
     Description: Return Grid with differences (represented by 1).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid_1 : Grid.
        2. grid_2 : Grid.
    ===========================================================================
     Return: Grid.
    ===========================================================================
    """
    return np.array(~(grid_1 == grid_2), dtype=int)


def distance(grid, idd_1, idd_2):
    """
    ===========================================================================
     Description: Return Manhattan Distance between 2 Nodes.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. idd_1 : int (Node's Id)
        3. idd_2 : int (Node's Id)
    ===========================================================================
    """
    row_1, col_1 = to_row_col(grid, idd_1)
    row_2, col_2 = to_row_col(grid, idd_2)
    
    return abs(row_1 - row_2) + abs(col_1 - col_2)


def get_dic_h(grid, goal, lookup=dict(), with_pathmax=False):
    """
    ===========================================================================
     Description: Return a Dictionary of Nodes of the Grid with their
                     Manhattan Distance to the Goal.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. goal : Node 
        3. lookup : dict int:int (Node.idd : accurate distance).
    ===========================================================================
     Return: dict int:(int,bool) (Node.idd : (h,is_lookup).
    ===========================================================================
    """        
    row_goal, col_goal = to_row_col(grid, goal)
    dic = dict()
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            idd = to_idd(grid,row,col)
            if not is_valid_idd(grid, idd): continue
            if (idd in lookup):
                dic[idd] = (lookup[idd],True)
            else:
                h = abs(row_goal - row) + abs(col_goal - col)
                dic[idd] = (h,False)
                
    if not with_pathmax: return dic
    
    """
    rebels = set()
    for idd in lookup:
        row, col = to_row_col(grid, idd)
        neighbors = get_neighbors(grid, row, col)
        for neighbor in neighbors:
            if dic[neighbor][0] < dic[idd][0]-1:
                dic[neighbor] = (dic[idd][0]-1,False)
                rebels.add(neighbor)
    pathmaxed_nodes = len(lookup)
    while rebels:
        idd = rebels.pop()
        row, col = to_row_col(grid, idd)
        neighbors = get_neighbors(grid, row, col)
        for neighbor in neighbors:           
            if dic[neighbor][0] < dic[idd][0]-1:
                dic[neighbor] = (dic[idd][0]-1,False)
                rebels.add(neighbor)
        pathmaxed_nodes += 1                                
    """
    
    rebels = set()
    for idd in lookup:
        row, col = to_row_col(grid, idd)
        neighbors = get_neighbors(grid, row, col)
        for neighbor in neighbors:
            if dic[neighbor][0] < dic[idd][0]-1:
                dic[neighbor] = (dic[idd][0]-1,False)
                rebels.add(neighbor)
    pathmaxed_nodes = len(lookup)
    for i in range(19):
        rebels_temp = rebels.copy()
        rebels.clear()
        for idd in rebels_temp:
            row, col = to_row_col(grid, idd)
            neighbors = get_neighbors(grid, row, col)
            for neighbor in neighbors:
                if dic[neighbor][0] < dic[idd][0]-1:
                    dic[neighbor] = (dic[idd][0]-1,False)
                    rebels.add(neighbor)
        pathmaxed_nodes += len(rebels_temp)   
        
    return dic, pathmaxed_nodes               


def to_dict_g(grid, start):
    """
    ============================================================================
     Description: Return Dict with G-Values of the nodes (Node.idd -> G-Value).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : Grid.
        2. start : int (Start Node's Id).
    ============================================================================
     Return: dict (int -> int) (Node.idd -> G-Value).
    ============================================================================
    """
    if not is_valid_idd(grid, start):
        return dict()
    opened = collections.deque([(start, 0)])
    closed = dict()    
    while opened:
        idd, g = opened.popleft()
        closed[idd] = g
        children = set(get_neighbors(grid,idd=idd))
        for child in children-closed.keys():
            opened.append((child,g+1))
    return closed


def to_dict_h(grid, goal):
    """
    ============================================================================
     Description: Return Dict with H-Values of the Nodes (Node.idd -> H-Value).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : Grid
        2. goal : int (Goal Node Id).
    ============================================================================
     Return: dict (int -> int) (Node.idd -> H-Value).
    ============================================================================
    """
    dict_h = dict()
    if not is_valid_idd(grid, goal):
        return dict_h
    for idd in get_valid_idds(grid):
        dict_h[idd] = distance(grid, idd, goal)
    return dict_h
        

def to_csv(grid, fr, lr, fc, lc, path):
    """
    ===========================================================================
     Description: Write Sub-Grid to CSV File.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. fr : int (First Row)
        3. lr : int (Last Row)
        4. fc : int (First Column)
        5. lc : int (Last Column)
        6. path : str (Path of CSV File)
    ===========================================================================
    """
    file = open(path, 'w')
    file.write(',')
    for col in range(fc,lc+1):
        file.write('{0},'.format(col))
    file.write('\n')
    for row in range(fr,lr+1):
        file.write('{0},'.format(row))
        for col in range(fc,lc+1):
            file.write('{0},'.format(grid[row][col]))
        file.write('\n')
    file.close()
        

