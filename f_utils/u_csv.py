import u_list

def create(path, li):
    """
    ===========================================================================
     Description: Create CSV File from List of Rows (Row is List of Strings).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (Path of CSV File to create).
        2. li : list of rows (Row is List of Strings).
    ===========================================================================
    """
    file = open(path,'w')
    for row in li:
        row = [str(val) for val in row]
        line = ','.join(row)
        file.write(line + '\n')
    file.close()
    
    
def to_list(path):
    """
    ===========================================================================
     Description: Convert CSV File into List of Rows (List of Strings).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (Path to CSV File).
    ===========================================================================
     Return: List of Rows (Row is a List of strings).
    ===========================================================================
    """
    file = open(path,'r')
    rows = list()
    for line in file:
        row = line.strip().split(',')
        rows.append(row)
    return rows


def to_dic(path, cols_key, cols_val, has_title=True):
    """
    ===========================================================================
     Description: Convert CSV File into Dictionary with specified columns
                     indices as Key and specified columns as Val.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (Path to CSV File).
        2. cols_key : list (List of requested key columns).
        3. cols_val : list (List of requested val columns).
        4. has_title : bool (Is the CSV File has title in the first row).
    ===========================================================================
     Return: dict (Dictionary that represents the CSV File).
    ===========================================================================
    """
    ans = dict()
    file = open(path,'r')
    for i, line in enumerate(file):
        if (has_title and i==0):
            continue
        vals = line.strip().split(',')
        key = u_list.sublist_by_index(vals,cols_key,index_start=1)
        val = u_list.sublist_by_index(vals,cols_val,index_start=1)
        key = tuple(key)
        val = tuple(val)
        ans[key] = val
    file.close()
    return ans


def repair(csv_in, csv_out, verbose=True):
    file_in = open(csv_in, 'r')
    file_out = open(csv_out, 'w')
