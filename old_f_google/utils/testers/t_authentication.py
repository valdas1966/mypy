from old_f_google.utils.generators.g_authentication import GenAuthentication


def test_rami() -> None:
    """
    ============================================================================
     Test Rami's Authentication (Credentials).
    ============================================================================
    """
    rami = GenAuthentication.gen_rami()
    assert rami.project_id == 'noteret'


def test_valdas() -> None:
    """
    ============================================================================
     Test Valdas's Authentication (Credentials).
    ============================================================================
    """
    valdas = GenAuthentication.gen_user()
    assert valdas.project_id == 'natural-nimbus-291415'
