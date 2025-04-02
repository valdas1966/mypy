from f_file.generators.g_1_txt import GenTXT


cd = 'd'
path = f'{cd}:\\temp\\test.txt'


def test_txt() -> None:
    """
    ========================================================================
     Test the TXT class.
    ========================================================================
    """
    txt = GenTXT.abcd(path=path)
    assert txt.read_lines() == ['ab', 'cd']
    txt.write_lines(lines=['ef'], append=True)
    assert txt.read_lines() == ['ab', 'cd', 'ef']
