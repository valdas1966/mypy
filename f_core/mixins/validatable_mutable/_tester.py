from f_core.mixins.validatable_mutable.main import ValidatableMutable


def test_validatable_mutable() -> None:
    """
    ========================================================================
     Test the ValidatableMutable class.
    ========================================================================
    """
    obj = ValidatableMutable(is_valid=True)
    assert obj
    obj.set_invalid()
    assert not obj
