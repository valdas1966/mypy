import pytest
from f_core.processes.i_3_parallel import ProcessParallel
from f_core.processes.i_3_parallel._factory import _square_chunk


@pytest.fixture
def io_bound() -> ProcessParallel[int, int]:
    """
    ============================================================================
     Create a thread-based ProcessParallel (happy path).
    ============================================================================
    """
    return ProcessParallel.Factory.io_bound()


@pytest.fixture
def cpu_bound() -> ProcessParallel[int, int]:
    """
    ============================================================================
     Create a process-based ProcessParallel (happy path).
    ============================================================================
    """
    return ProcessParallel.Factory.cpu_bound()


@pytest.fixture
def with_error() -> ProcessParallel[int, int]:
    """
    ============================================================================
     Create a ProcessParallel with a failing chunk.
    ============================================================================
    """
    return ProcessParallel.Factory.with_error()


def test_io_bound_run(io_bound: ProcessParallel[int, int]) -> None:
    """
    ============================================================================
     Test that thread-based execution produces correct sum-of-squares.
    ============================================================================
    """
    output = io_bound.run()
    assert len(output) == 3
    assert sum(output) == sum(x * x for x in range(1, 13))


def test_io_bound_no_errors(io_bound: ProcessParallel[int, int]) -> None:
    """
    ============================================================================
     Test that no errors are collected on success.
    ============================================================================
    """
    io_bound.run()
    assert io_bound.errors == []


def test_cpu_bound_run(cpu_bound: ProcessParallel[int, int]) -> None:
    """
    ============================================================================
     Test that process-based execution produces same results as threads.
    ============================================================================
    """
    output = cpu_bound.run()
    assert len(output) == 3
    assert sum(output) == sum(x * x for x in range(1, 13))


def test_tolerant_continues(with_error: ProcessParallel[int, int]) -> None:
    """
    ============================================================================
     Test that failed chunks produce None, others succeed.
    ============================================================================
    """
    output = with_error.run()
    # One chunk fails (contains 3 or 4), others succeed
    none_count = sum(1 for r in output if r is None)
    valid_count = sum(1 for r in output if r is not None)
    assert none_count >= 1
    assert valid_count >= 1


def test_tolerant_errors_collected(
        with_error: ProcessParallel[int, int]) -> None:
    """
    ============================================================================
     Test that errors are collected with correct structure.
    ============================================================================
    """
    with_error.run()
    assert len(with_error.errors) >= 1
    idx, chunk_data, exc = with_error.errors[0]
    assert isinstance(idx, int)
    assert isinstance(chunk_data, list)
    assert isinstance(exc, ValueError)


def test_workers_clamped() -> None:
    """
    ============================================================================
     Test that workers are clamped to input length.
    ============================================================================
    """
    proc = ProcessParallel(input=[1, 2],
                           func=_square_chunk,
                           workers=100)
    assert proc._workers == 2


def test_empty_input() -> None:
    """
    ============================================================================
     Test that empty input produces empty output and no errors.
    ============================================================================
    """
    proc = ProcessParallel(input=[],
                           func=_square_chunk,
                           workers=3)
    output = proc.run()
    assert output == []
    assert proc.errors == []


def test_run_idempotent(io_bound: ProcessParallel[int, int]) -> None:
    """
    ============================================================================
     Test that second run() produces same output and clears errors.
    ============================================================================
    """
    output_1 = io_bound.run()
    output_2 = io_bound.run()
    assert output_1 == output_2
    assert io_bound.errors == []
