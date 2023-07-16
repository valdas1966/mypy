from f_db.c_bq import BigQuery
from f_utils import u_file
from f_utils import u_csv


def load(folder: str,
         bq: BigQuery,
         tname='logger') -> None:
    """
    ============================================================================
     Description: Load Csv-Logger-Files into BigQuery.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. nodes : str (Csv-Logger Folder)
        2. bq : BigQuery (Connection-Class)
        3. tname : str (BigQuery Logger-Table-Name)
    ============================================================================
    """
    csvs = [f'{folder}\\{f}' for f in u_file.get_files_names(path=folder)]
    csv_out = f'{folder}\\out.csv'
    u_csv.append_files(csvs=csvs, csv_out=csv_out)
    d_rows = u_csv.to_dict_rows(csv=csv_out)
    bq.insert_rows(tname=tname, rows=d_rows)
    csvs.append(csv_out)
    u_file.delete(csvs)
