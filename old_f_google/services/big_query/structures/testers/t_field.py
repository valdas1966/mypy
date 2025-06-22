from old_f_google.big_query.structures.field import Field


def test_field() -> None:
    field = Field.string(name='a')
    assert field.name == 'a'
    assert field.dtype == 'STRING'
    