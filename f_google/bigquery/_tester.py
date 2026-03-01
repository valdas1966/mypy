from f_google.bigquery import BigQuery


def test_big_query() -> None:
    """
    ========================================================================
     Test select(), create(), insert_rows(), and drop().
    ========================================================================
    """
    tname = 'noteret.tiktok.test'
    bq = BigQuery.Factory.rami()
    cols = ['name string', 'age int64']
    bq.create(tname=tname, cols=cols)
    # Test create() and is_exists()
    assert bq.is_exists(tname=tname)
    rows = [{'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25}]
    bq.insert_rows(tname=tname, rows=rows)
    # Test insert_rows() and count()
    assert bq.count(tname=tname) == 2
    df = bq.select(query=tname)
    # Test select()
    assert len(df) == 2
    bq.drop(tname=tname)
    # Test drop()
    assert not bq.is_exists(tname=tname)
