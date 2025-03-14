from f_proj.rapid_api.data.i_0_audit import DataAudit


def test_not_ok() -> None:
    """
    ========================================================================
     Test the not_ok DataAudit.
    ========================================================================
    """
    params = {'msg': 'test', 'stam': 1}
    data = DataAudit.Gen.not_ok(status_code=400, params=params)
    assert data == {'is_ok': False, 'status_code': 400, 'msg': 'test'}


def test_not_found() -> None:
    """
    ========================================================================
     Test the not_found DataAudit.
    ========================================================================
    """
    params = {'msg': 'test'}
    data = DataAudit.Gen.not_found(params=params)
    assert data == {'is_ok': True, 'is_found': False, 'msg': 'test'}


def test_broken() -> None:
    """
    ========================================================================
     Test the broken DataAudit.
    ========================================================================
    """
    params = {'msg': 'test'}
    data = DataAudit.Gen.broken(msg='test', params=params)
    assert data == {'is_ok': True, 'is_found': True,
                    'is_broken': True, 'msg': 'test'}
    

def test_fill() -> None:
    """
    ========================================================================
     Test the fill method.
    ========================================================================
    """
    response = {'msg': 'test', 'stam': 1}
    data = DataAudit.Gen.valid(params=response)
    assert data == {'is_ok': True, 'is_found': True,
                    'is_broken': False, 'msg': 'test'}
