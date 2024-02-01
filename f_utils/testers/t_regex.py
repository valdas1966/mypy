from f_utils import u_regex


def test_extract_tels():
    text = '972511111111 גכעגכע 972522222222 asdgd 9725333333333 sdfsdf ' \
           '972544444444'
    tels = u_regex.extract_tels(text=text)
    assert tels == ['972511111111', '972522222222', '972544444444']
