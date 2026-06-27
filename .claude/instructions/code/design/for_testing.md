# Instruction to AI Agent (Claude Code): Testing Conventions

Tests live in `_tester.py` alongside `main.py`. Use pytest. Build test
objects by calling the **tested class's `Factory`** directly inside the
test body — **not** through a `@pytest.fixture` wrapper:

```python
def test_lt() -> None:
    """
    ========================================================================
     Test the __lt__() method.
    ========================================================================
    """
    a = Comparable.Factory.a()
    b = Comparable.Factory.b()
    assert a < b
    assert not (b < a)
```

- Test functions: `test_<method_name>()`.
- Each test has a docstring with `=` separators.
- Get canonical instances from the class's `Factory` (`Factory.a()`,
  `Factory.b()`, `Factory.gen()`) inside the test, so the inputs stay
  visible in the test body.

## Prefer `Factory` over `@pytest.fixture`

Do **not** wrap a `Factory` call in a `@pytest.fixture` when the
Factory method alone is enough. Fixtures add indirection and hide
where the object comes from:

```python
# AVOID — fixture duplicates Factory, adds no value
@pytest.fixture
def a() -> Comparable:
    return Comparable.Factory.a()

def test_lt(a: Comparable, b: Comparable) -> None:
    assert a < b
```

Use `@pytest.fixture` **only** when it adds real value beyond what
`Factory` provides — e.g., shared setup/teardown, parametrization,
scope (`scope='module'`), or an object built from multiple Factory
calls with non-trivial wiring. When in doubt, prefer `Factory`:
it's more explicit and keeps the test's inputs visible in the test
body.
