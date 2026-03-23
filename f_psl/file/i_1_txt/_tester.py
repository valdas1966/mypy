from f_psl.file.i_1_txt import FileTxt


def test_text() -> None:
    """
    ========================================================================
     Test text property (read and write).
    ========================================================================
    """
    f_empty = FileTxt.Factory.empty()
    f_hello = FileTxt.Factory.hello()
    assert f_empty.text == ''
    assert f_hello.text == 'hello'
    f_hello.text = 'world'
    assert f_hello.text == 'world'
    f_empty.delete()
    f_hello.delete()


def test_lines() -> None:
    """
    ========================================================================
     Test lines() method.
    ========================================================================
    """
    f_empty = FileTxt.Factory.empty()
    f_lines = FileTxt.Factory.lines()
    assert f_empty.lines() == []
    assert f_lines.lines() == ['aaa', 'bbb', 'ccc']
    f_empty.delete()
    f_lines.delete()


def test_write_line() -> None:
    """
    ========================================================================
     Test write_line() method.
    ========================================================================
    """
    f = FileTxt.Factory.empty()
    # Append (default)
    f.write_line('aaa')
    f.write_line('ccc')
    assert f.lines() == ['aaa', 'ccc']
    # Insert at index
    f.write_line('bbb', index=1)
    assert f.lines() == ['aaa', 'bbb', 'ccc']
    # Insert at beginning
    f.write_line('zzz', index=0)
    assert f.lines() == ['zzz', 'aaa', 'bbb', 'ccc']
    f.delete()


def test_delete_line() -> None:
    """
    ========================================================================
     Test delete_line() method.
    ========================================================================
    """
    f = FileTxt.Factory.lines()
    f.delete_line(index=1)
    assert f.lines() == ['aaa', 'ccc']
    f.delete_line(index=0)
    assert f.lines() == ['ccc']
    f.delete_line(index=-1)
    assert f.lines() == []
    f.delete()
