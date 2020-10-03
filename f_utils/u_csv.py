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


"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import u_tester
    import u_dir
   
    def tester_create():
        path_dir = 'c:\\tester_create'
        path_csv = path_dir + '\\test.csv'
        u_dir.create(path_dir)
    
        row_0 = ['a','b','c']
        row_1 = [1,2,3]
        row_2 = [4,5,6]
        li = [row_0, row_1, row_2]        
        create(path_csv,li)        
        li_test = to_list(path_csv)
        
        row_0_true = ['a','b','c']
        row_1_true = ['1','2','3']
        row_2_true = ['4','5','6']
        li_true = [row_0_true, row_1_true, row_2_true]        
        p1 = li_test == li_true
        u_dir.delete(path_dir)        
        u_tester.run(p1)
        
    def tester_to_dic():      
        path_dir = 'c:\\tester_create'
        path_csv = path_dir + '\\test.csv'
        u_dir.create(path_dir)
        
        row_0 = ['a','b','c']
        row_1 = [1,2,3]
        row_2 = [4,5,6]
        li = [row_0, row_1, row_2]
        create(path_csv, li)
        
        # One Key, One Val, With Title
        dic_test = to_dic(path_csv, cols_key=[1], cols_val=[3])
        dic_true = {('1',):('3',), ('4',):('6',)}
        p1 = dic_test == dic_true
        
        # One Key, One Val, Without Title
        dic_test = to_dic(path_csv, cols_key=[1], cols_val=[2], has_title=False)
        dic_true = {('a',):('b',), ('1',):('2',), ('4',):('5',)}
        p2 = dic_test == dic_true
        
        # Multi Key, One Val, Wit Title
        dic_test = to_dic(path_csv, cols_key=[1,2], cols_val=[3])
        dic_true = {('1','2'):('3',), ('4','5'):('6',)}
        p3 = dic_test == dic_true
        
        # Multi Key, Multi Val, With Title
        dic_test = to_dic(path_csv, cols_key=[1,2], cols_val=[2,3])
        dic_true = {('1','2'):('2','3'), ('4','5'):('5','6')}
        p4 = dic_test == dic_true
        
        u_dir.delete(path_dir)
        u_tester.run([p1,p2,p3,p4])        
            
    
    print('\n====================\nStart Tester\n====================')    
    tester_create()
    tester_to_dic()
    print('====================\nEnd Tester\n====================')            
    
tester()
            