from f_file.generators.g_1_csv import GenCSV


cd = 'd'
path = f'{cd}:\\temp\\test.csv'


def test_csv() -> None:
    """
    ========================================================================
     Test the CSV class.
    ========================================================================
    """
    csv = GenCSV.abcd(path=path)
    assert csv.read_titles() == ['title_1', 'title_2']
    assert csv.read_lines() == [['a', 'b'], ['c', 'd']]
    csv.write_lines(lines=[['e', 'f']], append=True)
    assert csv.read_lines() == [['a', 'b'], ['c', 'd'], ['e', 'f']]
