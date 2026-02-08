from f_core.mixins.validatable.main import Validatable


def test_validatable() -> None:
    """
    ========================================================================
     Test the Validatable class.
    ========================================================================
    """
    assert Validatable.Factory.valid()
    assert not Validatable.Factory.invalid()
