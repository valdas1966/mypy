from f_test.runner import TestRunner
from f_test.result import ResultTest


def test_run_on_hashable() -> None:
    """
    ========================================================================
     Test running testers on a known small folder (hashable has 1 test).
    ========================================================================
    """
    result = TestRunner.run(
        path_folder='f_core/mixins/hashable'
    )
    assert isinstance(result, ResultTest)
    assert result.files == 1
    assert result.passed >= 1
    assert result.is_passed


def test_run_on_empty_folder() -> None:
    """
    ========================================================================
     Test running on a folder with no _tester.py files.
    ========================================================================
    """
    result = TestRunner.run(path_folder='f_test/result')
    assert isinstance(result, ResultTest)
    assert result.files == 0
    assert result.total == 0
    assert result.is_passed


def test_result_str() -> None:
    """
    ========================================================================
     Test ResultTest __str__ formatting.
    ========================================================================
    """
    result = ResultTest(passed=5, failed=1, errors=0, files=3,
                        failures=['test_foo::test_bar'])
    s = str(result)
    assert 'FAILED' in s
    assert '5 passed' in s
    assert '1 failed' in s
    assert 'test_foo::test_bar' in s

    result_ok = ResultTest(passed=5, failed=0, errors=0, files=2)
    assert 'PASSED' in str(result_ok)
