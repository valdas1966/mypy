import cx_Oracle
import pandas as pd
from f_utils.c_res import Res


class Ora:

    format_date_dummy = 'yyyymmddhh24miss'
    str_date_dummy = '19000101000000'
    dict_dtypes = {'int64': 'int', 'object': 'varchar2(100)',
                   'float64': 'float'}
    
    #def __init__(self, user='n38100', password=None):
    def __init__(self, user='sys', password=None):
        """
        =======================================================================
         Descirption: Constructor - Init Attributes.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. user : str (User of Oracle).
            2. password : str (Password / User on None).
        =======================================================================
        """
        self.con = None
        self.user = user
        self.password = password
        if not password:
            self.password = user
        self.user = 'SYS'
        self.password = 'pass'

    def open(self):
        """
        =======================================================================
         Description: Open Connection to Oracle.
        =======================================================================
         Return: Res (bool).
        =======================================================================
        """
        dsn = cx_Oracle.makedsn('poramolam', '1522', service_name='olam')
        dsn = cx_Oracle.makedsn('localhost', '1521', service_name='oranew')
        try:
            self.con = cx_Oracle.connect(self.user, self.password, dsn,
                                         mode=cx_Oracle.SYSDBA,
                                         encoding='iso-8859-1',
                                         nencoding='iso-8859-1')
        except Exception as e:
            return Res(str(e), False)
        return Res()

    def run(self, command):
        """
        ===================================================================
         Description: Run an Command on Oralce.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. command : str (Command to Run).
        ===================================================================
         Return: Res (bool).
        ===================================================================
        """
        cur = self.con.cursor()
        try:
            cur.execute(command)
        except Exception as e:
            msg = '\n* Error in Oracle running command:\n** {0}\n*** {1}\n'.format(e, command)
            return Res(msg, False)
        return Res()

    def drop_table(self, tname):
        """
        ===================================================================
         Description: Drop Table from Oracle.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. tname : str (Table Name).
        ===================================================================
         Return: Res (bool).
        ===================================================================
        """
        return self.run('drop table {0}'.format(tname))

    def add_primary_key(self, tname, pk):
        """
        ===================================================================
         Description: Add Primary Key to Existed Table.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. tname : str (Table Name).
            2. pk : str (Column Names of Primary Key separated by comma).
        ===================================================================
         Return: Res (bool).
        ===================================================================
        """
        query = 'alter table {0} add constraint pk_{0} primary key({1})'
        return self.run(query.format(tname,pk))

    def create_table_as(self, tname, select, pk=None):
        """
        ===================================================================
         Description: Create Table as Select from another Table.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. tname : str (Table Name).
            2. select : str (Select Query).
            3. pk : str (Column Names separated by comma).
        ===================================================================
         Return: Res (bool).
        ===================================================================
        """
        self.drop_table(tname)
        query = 'create table {0} as {1}'
        res_create = self.run(query.format(tname, select))
        if not res_create:
            return res_create
        if pk:
            return self.add_primary_key(tname, pk)
        else:
            return Res()

    def create_table(self, tname, signature_cols, pk=None):
        """
        ===================================================================
         Description: Create Oracle Table by Signature Cols.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. tname : str (Table Name).
            2. signature_cols : str (Signature of Col-Name and Col-DType).
            3. pk : str (Primary Key, contains the names of the columns).
        ===================================================================
         Return: Res(bool).
        ===================================================================
        """
        self.drop_table(tname)
        str_command = f'create table {tname}({signature_cols})'
        res_create = self.run(str_command)
        if not res_create:
            return res_create
        if pk:
            return self.add_primary_key(tname, pk)
        else:
            return Res()

    def load(self, tname, df, pk=None):
        """
        ===================================================================
         Description: Load Data Frame into Oracle Table.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. tname : str (Table Name to Create).
            2. df : DataFrame.
            3. pk : str (Cols Names of Primary Key).
        ===================================================================
        """
        signature_cols = Ora.df_to_signature_cols(df)
        res_create = self.create_table(tname, signature_cols, pk)
        if not res_create:
            return res_create
        str_parameters = Ora.str_parameters(len(df.columns))
        command = f'insert into {tname} values({str_parameters})'
        cur = self.con.cursor()
        try:
            cur.executemany(command, df.values.tolist())
            self.con.commit()
        except Exception as e:
            msg = '\n* Error in Oracle Execute Many:\n** {0}\n*** {1}\n'.format(
                e, command)
            return Res(msg, False)
        return Res()

    def description(self, tname):
        """
        ===================================================================
         Description: Return Description of the Table's Columns.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. tname : str (Table Name).
        ===================================================================
         Return: Res (list).
        ===================================================================
        """
        query = 'select * from {0} where rownum=0'.format(tname)
        cur = self.con.cursor()
        try:
            cur.execute(query)
            return Res(cur.description)
        except Exception as e:
            msg = '\n* Error in Oracle running command:\n** '
            msg += '{0}\n*** {1}\n'.format(e, query)
            return Res(msg, False)

    def from_sas(self, tname_sas, tname_ora, pk=None):
        """
        ===================================================================
         Description: Canonize Table from SAS into Oracle format.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. tname_sas : str (Table Name from SAS).
            2. tname_ora : str (Table Name to Create).
        ===================================================================
         Return: Res (bool).
        ===================================================================
        """
        res_desc = self.description(tname_sas)
        if not res_desc:
            return Res(res_desc.msg, False)
        li_desc = [(col[0], col[1]) for col in res_desc.val]
        query = 'select '
        li_cols = list()
        for name, dtype in li_desc:
            dtype = str(dtype).lower()
            if 'char' in dtype or 'string' in dtype or 'clob' in dtype:
                li_cols.append("nvl(to_char({0}),'NULL') as {0}".format(name))
            elif 'date' in dtype or 'time' in dtype:
                li_cols.append(Ora.to_date_to_char(name))
            else:
                li_cols.append('nvl({0},-1) as {0}'.format(name))
        query += ','.join(li_cols)
        query += ' from {0} order by 1'.format(tname_sas)
        res_create = self.create_table_as(tname_ora, query)
        if not res_create:
            return res_create
        if pk:
            return self.add_primary_key(tname_ora, pk)
        else:
            return res_create

    def count(self, tname):
        """
        ===================================================================
         Description: Count rows in Oracle Table.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. tname : str (Table Name).
        ===================================================================
         Return: Res (int).
        ===================================================================
        """
        query = 'select count(*) from {0}'.format(tname)
        cur = self.con.cursor()
        try:
            cur.execute(query)
            return Res(cur.fetchone()[0])
        except Exception as e:
            return Res(str(e), False)

    def select(self, query):
        """
        ===================================================================
         Description: Select query into DataFrame.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. query : str (SQL Query or Table Name to select all table.
        ===================================================================
         Return: Res (DataFrame).
        ===================================================================
        """
        # if it is a table name
        if ' ' not in query:
            query = 'select * from {0}'.format(query)
        try:
            df = pd.read_sql(query, self.con)
            return Res(df)
        except Exception as e:
            return Res(str(e), False)

    def close(self):
        """
        ===================================================================
         Description: Close Connection to Oracle.
        =======================================================================
         Return: Res (bool).
        =======================================================================
        """
        try:
            self.con.close()
        except Exception as e:
            return Res(str(e), False)
        return Res()

    @staticmethod
    def to_date_to_char(col_date):
        """
        =======================================================================
         Description: Return str-representation of to_date-to_char query
                        when there is a column with strange date format.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. col_date : str (Name of Column with strange date format).
        =======================================================================
         Return: str (str-representation of to_date-to_char query.
        =======================================================================
        """
        str_inner = "to_date(to_char({0},'{1}'),'{1}')".format(col_date,
                                                               Ora.format_date_dummy)
        return "nvl({0},{1}) as {2}".format(str_inner, Ora.get_dummy_date(),
                                            col_date)

    @staticmethod
    def df_to_signature_cols(df):
        """
        ===================================================================
         Description: Return Signature of Columns in Data Frame.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. df : DataFrame.
        ===================================================================
         Return: str ex. 'col_1 int, col_2 varchar2(100), col_3 float'.
        ===================================================================
        """
        li = list()
        for name_col, dtype_col in df.dtypes.items():
            li.append(f'{name_col} {Ora.dict_dtypes[str(dtype_col)]}')
        return ', '.join(li)

    @staticmethod
    def str_parameters(n):
        """
        ===================================================================
         Description: Return str of parameters, ex: ':1, :2, :3'.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. n : int (Number of Parameters).
        ===================================================================
         Return: str.
        ===================================================================
        """
        li = [':' + str(x+1) for x in list(range(n))]
        return ', '.join(li)
