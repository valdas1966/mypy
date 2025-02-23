from f_file.generators.g_txt import GenTxt, Txt


def test_hello_world() -> None:
    """
    ========================================================================
     Test the hello_world Txt object.
    ========================================================================
    """
    txt_1 = GenTxt.hello_world()
    txt_2 = Txt(path=txt_1.path)
    txt_1.delete()
    assert txt_1.lines == txt_2.lines


def test_length_line_max() -> None:
    """
    ========================================================================
     Test the length_line_max method.
    ========================================================================
    """ 
    txt = GenTxt.hello_world()
    length_line_max = txt.length_line_max()
    txt.delete()
    assert length_line_max == 5
