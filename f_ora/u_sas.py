from f_ora import u_ora


def download_table(tname, pk=None):
    """
    =======================================================================
     Description: Download Table from Sas (correcting data types and pk).
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. tname : str (Table Name).
        2. pk : str (Column Names of the Primary Key).
    =======================================================================
     Return: Res (bool).
    =======================================================================
    """
    tname_old = 'temp_{0}'.format(tname)
    res_desc = u_ora.description(tname_old)
    if not res_desc:
        return res_desc
    col_names = _correct_dtypes(res_desc.val)
    query = 'select {0} from {1}'.format(col_names, tname_old)
    res_create = u_ora.create_table_as(tname, query, pk, with_doc=True)
    return res_create


def _correct_dtypes(li_desc):
    li_names = list()
    for col in li_desc:
        name = col[0]
        dtype = str(col[1])
        if 'CLOB' in dtype:
            name = 'to_char({0}) as {0}'.format(name)
        li_names.append(name)
    return ', '.join(li_names)



#print(download_table('coupling_tel_father','tel, pid_father'))
#print(download_table('coupling_tel_pid', 'tel, pid'))
#print(download_table('israel_carteset', 'tel, pid, taz'))
#print(download_table('israel_pid', 'pid, taz'))
print(download_table('israel_kinship', 'pid_a, pid_b'))
#print(download_table('israel_conns', 'tel_a, tel_b'))
#print(download_table('names_parents','name_parent'))
#print(download_table('israel_meapp_all','tel, name'))



