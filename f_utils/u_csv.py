import u_list
import pandas as pd


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


def repair(csv_in, csv_out, csv_errors=None, verbose=True):
    file_in = open(csv_in, 'r')
    file_out = open(csv_out, 'w')
    file_errors = None
    if csv_errors:
            file_errors = open(csv_errors, 'w')
    line = True
    cnt_errors = 0
    i = 1
    while not line == '':
        try:
            line = file_in.readline()
            if line:
                file_out.write(line)
        except Exception as _:
            cnt_errors += 1
            if csv_errors:
                file_errors.write(f'{i}\n')
        i += 1
    if verbose:
        print(f'Repair CSV: {csv_in}')
        print(f'{i-cnt_errors} Success, {cnt_errors} Errors')


def append(csv_1, csv_2, csv_out, verbose=True):
    df_1 = pd.read_csv(csv_1)
    df_2 = pd.read_csv(csv_2)
    df_out = df_1.append(df_2)
    df_out.to_csv(csv_out)
    if verbose:
        print(f'{csv_1} [{len(df_1)} rows]')
        print('append vs')
        print(f'{csv_2} [{len(df_2)} rows]')
        print(f'into {csv_out}')
        print(f'[{len(df_out)} rows]')

