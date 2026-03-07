from f_google.services.sheets.spread import Spread


def test_name_spread() -> None:
    """
    ========================================================================
     Test that Spreadsheet name is returned.
    ========================================================================
    """
    spread = Spread.Factory.valdas_test()
    assert spread.name == 'Test'


def test_len_sheets() -> None:
    """
    ========================================================================
     Test that Worksheets are returned.
    ========================================================================
    """
    spread = Spread.Factory.valdas_test()
    sheets = spread.sheets
    assert len(sheets) == 1


def test_name_sheet() -> None:
    """
    ========================================================================
     Test accessing a Sheet by name.
    ========================================================================
    """
    spread = Spread.Factory.valdas_test()
    name_sheet = spread.sheets[0].name
    assert name_sheet == 'Sheet1'


def test_cell_value() -> None:
    """
    ========================================================================
     Test accessing a Cell value via Sheet[row][col].
    ========================================================================
    """
    spread = Spread.Factory.valdas_test()
    sheet = spread.sheets[0]
    value = sheet[1][0]
    assert value == 'Hello2'


def test_last_row() -> None:
    """
    ========================================================================
     Test Sheet last_row().
    ========================================================================
    """
    spread = Spread.Factory.valdas_test()
    sheet = spread.sheets[0]
    assert sheet.last_row() >= 0


def test_last_col() -> None:
    """
    ========================================================================
     Test Sheet last_col().
    ========================================================================
    """
    spread = Spread.Factory.valdas_test()
    sheet = spread.sheets[0]
    assert sheet.last_col() >= 0


def test_to_range() -> None:
    """
    ========================================================================
     Test Sheet to_range() returns a Range with correct shape.
    ========================================================================
    """
    spread = Spread.Factory.valdas_test()
    sheet = spread.sheets[0]
    r = sheet.to_range()
    assert r[1][0] == 'Hello2'
