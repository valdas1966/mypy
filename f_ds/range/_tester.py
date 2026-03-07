from f_ds.range import Range


def test_getitem() -> None:
    """
    ========================================================================
     Test __getitem__().
    ========================================================================
    """
    ran = Range.Factory.without_header()
    assert ran[0] == ['r0c0', 'r0c1', 'r0c2']
    assert ran[2] == ['r2c0', 'r2c1', 'r2c2']
    assert ran[1][1] == 'r1c1'


def test_to_df() -> None:
    """
    ========================================================================
     Test to_df() with header=True.
    ========================================================================
    """
    ran = Range.Factory.with_header()
    df = ran.to_df()
    assert list(df.columns) == ['Name', 'Age', 'City']
    assert df.shape == (2, 3)
    assert df.iloc[0]['Name'] == 'Alice'
