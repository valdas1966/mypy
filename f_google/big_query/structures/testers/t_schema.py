from f_google.big_query.structures.schema import Schema, Field


def test_add() -> None:
    field_a = Field(name='a', dtype=Field.STRING)
    field_b = Field(name='b', dtype=Field.INTEGER)
    schema_a = Schema()
    schema_a.add(field_a)
    schema_b = Schema()
    schema_b.add(field_b)
    schema_c = schema_a + schema_b
    assert schema_c.to_list() == [field_a, field_b]
