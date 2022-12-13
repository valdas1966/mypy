from f_utils import u_list
from f_utils import u_file
import pandas as pd


def create(path: str,
           header: 'list of obj' = None,
           rows: 'list of list of obj' = None) -> None:
    """
    ===========================================================================
     Description: Create CSV-File [Empty | Header | Rows]
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (Path to Create).
        2. header: list[obh] (List of Column-Names).
        2. rows: list[list[obj]]
    ===========================================================================
    """
    def __write_line(vals):
        vals = [str(val) for val in vals]
        line = ','.join(vals)
        file.write(f'{line}\n')

    file = open(path, 'w')
    if header:
        __write_line(vals=header)
    if rows:
        for row in rows:
            __write_line(vals=row)
    file.close()


def append(path: str, row: 'list of obj') -> None:
    """
    ============================================================================
     Description: Append New-Line into CSV-File.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str [CSV-File Path].
        2. row : list[obj] [List of Row-Values].
    ============================================================================
    """
    file = open(path, 'a')
    vals = [str(val) for val in row]
    line = ','.join(vals)
    file.write(f'{line}\n')
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


def append_files(csvs: 'list of str',
                 csv_out: str) -> None:
    """
    ============================================================================
     Description: Append Csv-Files into one Csv-File.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. csvs : list[str] (List of Csv-Paths).
        2. csv_out : str (Csv-Out-Path).
    ============================================================================
    """
    dfs = [pd.read_csv(csv) for csv in csvs]
    df_all = pd.concat(dfs)
    df_all.to_csv(csv_out, index=None)


def to_dict_rows(csv: str) -> 'list of dict':
    """
    ============================================================================
     Description: Convert Csv-File into List of Dict-Rows (Ready to BigQuery).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. csv : str (Csv-Path).
    ============================================================================
    """
    lines = u_file.read(csv).split('\n')
    keys = lines[0].split(',')
    rows = list()
    for i in range(1, len(keys)):
        vals = lines[i].split(',')
        vals = [None if val == 'None' else val for val in vals]
        d_row = dict(zip(keys, vals))
        rows.append(d_row)
    return rows
