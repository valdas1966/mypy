from f_os import u_environ


def test_get_set():
    name = 'a'
    value = 'b'
    u_environ.set(name, value)
    assert u_environ.get(name) == value
    u_environ.remove(name)


def test_remove():
    name = 'a'
    value = 'b'
    u_environ.set(name, value)
    u_environ.remove(name)
    assert not u_environ.get(name)
