from f_file_old.generators.g_1_csv import GenCSV, CSV


cd = 'd'
path = f'{cd}:\\temp\\test.csv'
path_1 = f'{cd}:\\temp\\test_1.csv'
path_2 = f'{cd}:\\temp\\test_2.csv'


def test_csv() -> None:
    """
    ========================================================================
     Test the CSV class.
    ========================================================================
    """
    csv = GenCSV.abcd(path=path)
    assert csv.titles == ['title_1', 'title_2']
    assert csv.read_lines() == [['a', 'b'], ['c', 'd']]
    csv.write_lines(lines=[['e', 'f']])
    assert csv.read_lines() == [['a', 'b'], ['c', 'd'], ['e', 'f']]
    dicts = [{'title_2': 'g', 'title_1': 'h'}]
    csv.write_dicts(dicts=dicts)
    assert csv.read_lines() == [['a', 'b'], ['c', 'd'], ['e', 'f'], ['h', 'g']]


def test_union() -> None:
    """
    ========================================================================
     Test the union method.
    ========================================================================
    """
    GenCSV.abcd(path=path_1)
    GenCSV.abcd(path=path_2)
    paths_in = [path_1, path_2]
    path_out = path
    csv = CSV.union(paths_in=paths_in, path_out=path_out)
    assert csv.titles == ['title_1', 'title_2']
    assert csv.read_lines() == [['a', 'b'], ['c', 'd'], ['a', 'b'], ['c', 'd']]
