from f_utils.c_res import Res
from f_ora.c_ora import Ora
from f_utils.c_timer import Timer


def run(command, user='n38100'):
    """
    =======================================================================
     Description: Connect to Oracle, Run a Command, Close the Connection.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. command : str (Command to Run).
        2. user : str (Oracle User to connect).
    =======================================================================
     Return: Res (bool).
    =======================================================================
    """
    ora = Ora(user)
    res = ora.open()
    if not res:
        return res
    res = ora.run(command)
    ora.close()
    return res


def description(tname, user='n38100'):
    """
    =======================================================================
     Description: Return Columns description of the Table.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. tname : str (Table Name).
        2. user : str (Oracle User).
    =======================================================================
     Return: Res (list).
    =======================================================================
    """
    ora = Ora(user)
    res = ora.open()
    if not res:
        return res
    res = ora.description(tname)
    ora.close()
    return res


def drop_table(tname, user='n38100'):
    """
    =======================================================================
     Description: Drop Table in Oracle.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. tname : str (Table Name).
        2. user : str (Oracle User).
    =======================================================================
     Return: Res (bool).
    =======================================================================
    """
    ora = Ora(user)
    res_open = ora.open()
    if not res_open:
        return res_open
    res_drop = ora.drop_table(tname)
    ora.close()
    return res_drop


def create_table_as(tname, select, pk=None, with_doc=False, user='n38100'):
    """
    =======================================================================
     Description: Create Table as Select from another Table.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. tname : str (Table Name).
        2. select : str (Select Query).
        3. pk : str (Column Names of the Primary Key separated by comma).
        4. user : str (Oracle User).
    =======================================================================
     Return: Res (bool).
    =======================================================================
    """
    timer = Timer()
    ora = Ora(user)
    res_open = ora.open()
    if not res_open:
        return res_open
    res_create = ora.create_table_as(tname, select, pk)
    count = 0
    if res_create and with_doc:
        count = f'{ora.count(tname).val:,}'
    ora.close()
    elapsed = timer.elapsed()
    if res_create and with_doc:
        msg = 'Table [{0}] with [{1}] rows was successfully created in a [{2}] seconds'
        print(msg.format(tname, count, elapsed))
    return res_create


def create_tables(li, user='n38100'):
    """
    =======================================================================
     Description: Run a sequence of Create Table As commands.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. li : list of tuples (tname, query, pk[optional]).
        2. user : str (Oracle User).
    =======================================================================
     Return: Res (bool).
    =======================================================================
    """
    timer = Timer()
    ora = Ora(user)
    res_open = ora.open()
    if not res_open:
        return res_open
    for t in li:
        tname = t[0]
        query = t[1]
        pk = t[2] if len(t) == 3 else None
        res_create = ora.create_table_as(tname, query, pk)
        count = 0
        if res_create:
            count = f'{ora.count(tname).val:,}'
            elapsed = timer.elapsed()
            msg = 'Table [{0}] with [{1}] rows was successfully created in a [{2}] seconds'
            print(msg.format(tname, count, elapsed))
        else:
            return res_create
    ora.close()
    return res_open


def count(tname, user='n38100'):
    """
    =======================================================================
     Description: Count rows in Oracle Table.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. tname : str (Table Name).
        2. user : str (Oracle User).
    =======================================================================
     Return: Res (int).
    =======================================================================
    """
    ora = Ora(user)
    res_open = ora.open()
    if not res_open:
        return res_open
    res_count = ora.count(tname)
    ora.close()
    return res_count


def select(query, user='n38100'):
    """
    =======================================================================
     Description: Select table into DataFrame.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. query : str (Query or Table Name to Select).
        2. user : str (Oracle User).
    =======================================================================
     Return: Res (DataFrame).
    =======================================================================
    """
    ora = Ora(user)
    res_open = ora.open()
    if not res_open:
        return res_open
    res_select = ora.select(query)
    ora.close()
    return res_select

def from_sas(tname_sas, tname_ora, pk, user='n38100'):
    """
    =======================================================================
     Description: Canonize Table from SAS into Oracle format.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. tname_sas : str (Table Name from SAS).
        2. tname_ora : str (Table Name to Create).
        3. user : str (Oracle User).
    =======================================================================
     Return: Res (bool).
    =======================================================================
    """
    ora = Ora(user)
    res_open = ora.open()
    if not res_open:
        return res_open
    res_from_sas = ora.from_sas(tname_sas, tname_ora, pk)
    ora.close()
    return res_from_sas


def get_empty_cols(tname, user='n38100'):
    empty_cols = set()
    ora = Ora(user)
    res_open = ora.open()
    if not res_open:
        return res_open
    res_desc = ora.description(tname)
    if not res_desc:
        ora.close()
        return res_desc
    for col in res_desc.val:
        query = 'select count(*) from {0} where {1} is not null'.format(tname, col)
        res_count = ora.select(query)
        if not res_count:
            ora.close()
            return res_count
        values = res_count.val.iloc[0][0]
        if not values:
            empty_cols.add(col)
    ora.close()
    return Res(empty_cols)


def load(tname, df, pk=None, user='n38100'):
    """
    =======================================================================
     Description: Load DataFrame into Oracle Table.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. tname : str (Table Name to Create).
        2. df : DataFrame (with data to load).
        3. user : str (Oracle User Name).
    =======================================================================
     Return: Res(bool).
    =======================================================================
    """
    ora = Ora(user)
    res_open = ora.open()
    if not res_open:
        return res_open
    res_load = ora.load(tname, df, pk)
    ora.close()
    return res_load
