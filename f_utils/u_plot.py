import matplotlib.pyplot as plt
import u_grid

def plot_grid(grid, special_rows_cols=[], special_colors=[], path=None):
    """
    ===========================================================================
     Description - Plot Grid with black and white or special colors.
    ---------------------------------------------------------------------------
        1. Plot special cells with special colors.
        2. Other cells plot with black and white colors (valid xyable or not).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. grid : Grid
        2. special_rows_cols : list of list of tuples of row and col.
        3. special_colors : list of 3-element tuples (RGB representation).
        4. path : str (where to store the picture file).
    ===========================================================================
    """    
    arr = [[(-1,-1,-1) for x in range(grid.shape[1])] for y in range(grid.shape[0])]
    
    for i, rows_cols in enumerate(special_rows_cols):
        color = special_colors[i]
        for row, col in rows_cols:
            arr[row][col] = color
            
    for idd in range(grid.size):
        row, col = u_grid.to_row_col(grid, idd)        
        if arr[row][col] == (-1,-1,-1):    
            if u_grid.is_valid_idd(grid, idd):
                arr[row][col] = (255,255,255)
            else:
                arr[row][col] = (0,0,0)

    fig, ax = plt.subplots()
    ax.imshow(arr)    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
    fig.tight_layout()
    plt.show()
    
    if (path):
        plt.savefig(path)
        
 