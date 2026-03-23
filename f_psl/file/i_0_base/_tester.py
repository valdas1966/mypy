from f_psl.file.i_0_base import FileBase


def test_exists() -> None:
    """
    ========================================================================
     Test exists() for existing and deleted files.
    ========================================================================
    """
    f = FileBase.Factory.empty()
    assert f.exists()
    f.delete()
    assert not f.exists()


def test_name() -> None:
    """
    ========================================================================
     Test the name property.
    ========================================================================
    """
    f_empty = FileBase.Factory.empty()
    f_hello = FileBase.Factory.hello()
    assert f_empty.name == 'empty.tmp'
    assert f_hello.name == 'hello.txt'
    f_empty.delete()
    f_hello.delete()


def test_stem() -> None:
    """
    ========================================================================
     Test the stem property.
    ========================================================================
    """
    f_empty = FileBase.Factory.empty()
    f_hello = FileBase.Factory.hello()
    assert f_empty.stem == 'empty'
    assert f_hello.stem == 'hello'
    f_empty.delete()
    f_hello.delete()


def test_suffix() -> None:
    """
    ========================================================================
     Test the suffix property.
    ========================================================================
    """
    f_empty = FileBase.Factory.empty()
    f_hello = FileBase.Factory.hello()
    assert f_empty.suffix == '.tmp'
    assert f_hello.suffix == '.txt'
    f_empty.delete()
    f_hello.delete()


def test_size() -> None:
    """
    ========================================================================
     Test file size in bytes.
    ========================================================================
    """
    f_empty = FileBase.Factory.empty()
    f_hello = FileBase.Factory.hello()
    assert f_empty.size == 0
    assert f_hello.size == 5
    f_empty.delete()
    f_hello.delete()


def test_delete() -> None:
    """
    ========================================================================
     Test that delete removes the file and does not raise twice.
    ========================================================================
    """
    f = FileBase.Factory.empty()
    assert f.exists()
    f.delete()
    assert not f.exists()


def test_str() -> None:
    """
    ========================================================================
     Test the __str__() and __repr__() methods.
    ========================================================================
    """
    f = FileBase.Factory.empty()
    assert str(f) == str(f.path)
    assert repr(f).startswith('<FileBase:')
    f.delete()
