import collections

import pytest

from f_core.imports import ULazy


def test_install() -> None:
    """
    ========================================================================
     Test ULazy.install() across:
      * symbol form ('module:attr') resolves the attribute,
      * module form ('module') returns the module itself,
      * resolved value is cached into the package globals,
      * __all__ lists the public names,
      * __dir__ lists the public names,
      * unknown attribute raises AttributeError.
    ========================================================================
    """
    # Symbol form resolves the attribute
    g = {'__name__': 'fake.pkg'}
    ULazy.install(g=g, specs={'OD': 'collections:OrderedDict'})
    actual = g['__getattr__']('OD')
    expected = collections.OrderedDict
    assert actual is expected

    # Module form (no colon) returns the module
    g = {'__name__': 'fake.pkg'}
    ULazy.install(g=g, specs={'coll': 'collections'})
    actual = g['__getattr__']('coll')
    expected = collections
    assert actual is expected

    # Resolved value is cached into the package globals
    g = {'__name__': 'fake.pkg'}
    ULazy.install(g=g, specs={'OD': 'collections:OrderedDict'})
    g['__getattr__']('OD')
    actual = g['OD']
    expected = collections.OrderedDict
    assert actual is expected

    # __all__ lists the public names
    g = {'__name__': 'fake.pkg'}
    ULazy.install(g=g, specs={'OD': 'collections:OrderedDict'})
    actual = g['__all__']
    expected = ['OD']
    assert actual == expected

    # __dir__ lists the public names
    g = {'__name__': 'fake.pkg'}
    ULazy.install(g=g, specs={'OD': 'collections:OrderedDict'})
    actual = g['__dir__']()
    expected = ['OD']
    assert actual == expected

    # Relative spec resolves against the calling package
    g = {'__name__': 'collections.abc', '__package__': 'collections'}
    ULazy.install(g=g, specs={'OD': '.:OrderedDict'})
    actual = g['__getattr__']('OD')
    expected = collections.OrderedDict
    assert actual is expected

    # Unknown attribute raises AttributeError
    g = {'__name__': 'fake.pkg'}
    ULazy.install(g=g, specs={'OD': 'collections:OrderedDict'})
    with pytest.raises(AttributeError):
        g['__getattr__']('missing')
