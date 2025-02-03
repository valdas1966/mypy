from f_core.components.generators.g_enum_callable import GenEnumCallable


def test_enum_callable() -> None:
    """
    ========================================================================
     Test the EnumCallable.
    ========================================================================
    """
    type_a = GenEnumCallable.gen_a()
    assert type_a.A().name == 'A'
    assert type_a.B().name == 'B'
    assert type_a.C().name == 'C'
