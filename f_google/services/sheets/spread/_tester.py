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
    return Spread.Factory.test()


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


def test_set_cell_value(sheet: Sheet) -> None:
    """
    ========================================================================
     Test writing a Cell value and reading it back.
    ========================================================================
    """
    original = str(sheet[0][0])
    sheet[0][0].value = 'TestWrite'
    assert sheet[0][0] == 'TestWrite'
    # Restore original value
    sheet[0][0].value = original
    assert sheet[0][0] == original


def test_insert_row(sheet: Sheet) -> None:
    """
    ========================================================================
     Test inserting an empty row and then removing it.
    ========================================================================
    """
    original_last = sheet.last_row()
    original_row_2 = str(sheet[1][0])
    # Insert empty row at position 2 (1-based)
    sheet.insert_row(row=2)
    assert sheet.last_row() == original_last + 1
    assert sheet[1][0] == ''
    assert sheet[2][0] == original_row_2
    # Clean up: delete the inserted row
    sheet.delete_row(row=2)
    assert sheet.last_row() == original_last


def test_delete_row(sheet: Sheet) -> None:
    """
    ========================================================================
     Test deleting a row and then restoring it.
    ========================================================================
    """
    original_last = sheet.last_row()
    original_row_2 = [str(c) for c in sheet[1]]
    original_row_3 = str(sheet[2][0])
    # Delete row 2 (1-based)
    sheet.delete_row(row=2)
    assert sheet.last_row() == original_last - 1
    assert sheet[1][0] == original_row_3
    # Restore: insert row back and fill values
    sheet.insert_row(row=2)
    for col, val in enumerate(original_row_2):
        if val:
            sheet[1][col].value = val
    assert sheet.last_row() == original_last
    assert sheet[1][0] == original_row_2[0]
