from f_google.sheets import Sheets


def test_name() -> None:
    """
    ========================================================================
     Test that Spreadsheet name is returned.
    ========================================================================
    """
    sheets = Sheets.Factory.valdas(
        id_spread='1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'
    )
    print(sheets.name)
    assert sheets.name


def test_sheet_names() -> None:
    """
    ========================================================================
     Test that Worksheet names are returned.
    ========================================================================
    """
    sheets = Sheets.Factory.valdas(
        id_spread='1LqiT2mBYlo1i2M6tabj8s9kiEHngffg4dYY7-amPbgw'
    )
    names = sheets.sheet_names
    print(names)
    assert names
