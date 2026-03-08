import pytest
from f_google.services.sheets.spread import Spread
from f_google.services.sheets.sheet import Sheet


@pytest.fixture(scope='module')
def spread() -> Spread:
    """
    ========================================================================
     Create a test Spread (loaded once per module).
    ========================================================================
    """
    return Spread.Factory.valdas_test()


@pytest.fixture(scope='module')
def sheet(spread: Spread) -> Sheet:
    """
    ========================================================================
     Get the first Sheet from the test Spread.
    ========================================================================
    """
    return spread.sheets[0]


def test_name_spread(spread: Spread) -> None:
    """
    ========================================================================
     Test that Spreadsheet name is returned.
    ========================================================================
    """
    assert spread.name == 'Test'


def test_len_sheets(spread: Spread) -> None:
    """
    ========================================================================
     Test that Worksheets are returned.
    ========================================================================
    """
    assert len(spread.sheets) == 1


def test_name_sheet(sheet: Sheet) -> None:
    """
    ========================================================================
     Test accessing a Sheet by name.
    ========================================================================
    """
    assert sheet.name == 'Sheet1'


def test_cell_value(sheet: Sheet) -> None:
    """
    ========================================================================
     Test accessing a Cell value via Sheet[row][col].
    ========================================================================
    """
    assert sheet[1][0] == 'Hello2'


def test_last_row(sheet: Sheet) -> None:
    """
    ========================================================================
     Test Sheet last_row().
    ========================================================================
    """
    assert sheet.last_row() == 3


def test_last_col(sheet: Sheet) -> None:
    """
    ========================================================================
     Test Sheet last_col().
    ========================================================================
    """
    assert sheet.last_col() == 4


def test_to_range(sheet: Sheet) -> None:
    """
    ========================================================================
     Test Sheet to_range() returns a Range with correct shape.
    ========================================================================
    """
    r = sheet.to_range()
    assert r[1][0] == 'Hello2'
