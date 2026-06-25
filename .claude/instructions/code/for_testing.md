# Instruction to AI Agent (Claude Code): Testing Conventions

Tests live in `_tester.py` alongside `main.py`. Use pytest with fixtures that call Factory methods:
```python
import pytest

@pytest.fixture
def a() -> Comparable:
    """
    ========================================================================
     Create a Comparable object with the value 'A'.
    ========================================================================
    """
    return Comparable.Factory.a()

def test_lt(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __lt__() method.
    ========================================================================
    """
    assert a < b
    assert not (b < a)
```

- Test functions: `test_<method_name>()`.
- Fixtures: short names matching Factory methods (`a`, `b`, `gen`).
- Each test has a docstring with `=` separators.

## Prefer `Factory` over `@pytest.fixture`

Do **not** wrap a `Factory` call in a `@pytest.fixture` when the
Factory method alone is enough. Fixtures add indirection and hide
where the object comes from — if the test just needs a canonical
instance, call `MyClass.Factory.a()` directly inside the test:

```python
# GOOD — Factory is the single source of canonical test objects
def test_lt() -> None:
    """
    ========================================================================
     Test the __lt__() method.
    ========================================================================
    """
    a = Comparable.Factory.a()
    b = Comparable.Factory.b()
    assert a < b

# AVOID — fixture duplicates Factory, adds no value
@pytest.fixture
def a() -> Comparable:
    return Comparable.Factory.a()
```

Use `@pytest.fixture` **only** when it adds real value beyond what
`Factory` provides — e.g., shared setup/teardown, parametrization,
scope (`scope='module'`), or an object built from multiple Factory
calls with non-trivial wiring. When in doubt, prefer `Factory`:
it's more explicit and keeps the test's inputs visible in the test
body.
