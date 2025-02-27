from collections.abc import Iterable
from dataclasses import dataclass 
import pandas as pd
import os


class GenCSV:
    """
    ========================================================================
     Generator for CSV files.
    ========================================================================
    """

    @staticmethod
    def from_dataclass(data: dataclass | Iterable[dataclass],
                       path: str,
                       delimiter: str = ',') -> None:
        """
        ========================================================================
         Generate a CSV-file from a dataclass or an iterable of dataclasses.
        ========================================================================
        """
        # if file exists, delete it
        if os.path.exists(path):
            os.remove(path)

        # if data is a dataclass, convert it to a list[dataclass]
        rows = [data] if isinstance(data, dataclass) else rows

        # create the file
        with open(path, 'w') as f:
            f.write(data)

        # write the header of the fields
        f.write(delimiter.join(rows[0].__dict__.keys()))
        f.write('\n')

        # for each row, write the data with the delimiter between
        #  the fields and a new line at the end of the row
        for row in rows:
            f.write(delimiter.join(row))
            f.write('\n')

        # save and close the file
        f.save()
        f.close()

    @staticmethod
    def from_df(df: pd.DataFrame,
                path: str,
                delimiter: str = ',') -> None:
        """
        ========================================================================
         Generate a CSV-file from a pandas DataFrame.
        ========================================================================
        """
        # if file exists, delete it
        if os.path.exists(path):
            os.remove(path)

        # write the DataFrame to the file
        df.to_csv(path, delimiter=delimiter)        
