from f_file_old.generators.g_csv import GenCSV, dataclass


def test_from_dataclass():
    """
    ========================================================================
     Test the from_dataclass method.
    ========================================================================
    """
    @dataclass
    class Data:
        name: str
        age: int

    # create the data
    data_1 = Data(name='John', age=30)
    data_2 = Data(name='Jane', age=25)
    data = [data_1, data_2]

    # generate the CSV file
    GenCSV.from_dataclass(data=data, path='g:\\temp\\test.csv')

