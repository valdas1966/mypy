from old_f_google.user import User
import os


def test_rami():
    """
    ============================================================================
     Test if file exists and is readable.
    ============================================================================
    """
    user = User.RAMI
    assert os.path.exists(user), f"File {user} does not exist"
    with open(user, 'r') as f:
        assert f.readable(), f"File {user} cannot be opened"


def test_valdas():
    """
    ============================================================================
     Test if file exists and is readable.
    ============================================================================
    """     
    user = User.VALDAS
    assert os.path.exists(user), f"File {user} does not exist"
    with open(user, 'r') as f:
        assert f.readable(), f"File {user} cannot be opened"
