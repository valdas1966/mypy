from f_proj.rapid_api.data.i_0_audit import DataAudit


def test_is_not_ok():
    data = DataAudit.gen_is_not_ok(status_code=400,
                                   params={'is_found': True, 'stam': 1})
    
    assert data['is_ok'] == False
    assert data['code'] == 400
    assert data['is_found'] == True

