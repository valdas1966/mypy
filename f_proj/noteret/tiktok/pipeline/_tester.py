from f_proj.noteret.tiktok.pipeline import PipelineInsert
from f_proj.rapid_api.tiktok import ApiTikTok
import pytest


def test_registry_not_empty() -> None:
    """
    ============================================================================
     Test that the registry has entries.
    ============================================================================
    """
    assert len(PipelineInsert._REGISTRY) > 0


def test_registry_tables_not_empty() -> None:
    """
    ============================================================================
     Test that every registry entry has non-empty table names.
    ============================================================================
    """
    for name, (tname, tname_todo, _) in PipelineInsert._REGISTRY.items():
        assert tname, f'{name}: tname is empty'
        assert tname_todo, f'{name}: tname_todo is empty'


def test_registry_funcs_callable() -> None:
    """
    ============================================================================
     Test that every registry entry has a callable function.
    ============================================================================
    """
    for name, (_, _, func) in PipelineInsert._REGISTRY.items():
        assert callable(func), f'{name}: func is not callable'


def test_registry_funcs_match_api() -> None:
    """
    ============================================================================
     Test that every registry function exists on ApiTikTok.
    ============================================================================
    """
    for name, (_, _, func) in PipelineInsert._REGISTRY.items():
        api_func = getattr(ApiTikTok, name, None)
        if api_func is not None:
            assert func == api_func, (
                f'{name}: registry func does not match '
                f'ApiTikTok.{name}')


def test_registry_table_prefix() -> None:
    """
    ============================================================================
     Test that all table names start with the expected prefix.
    ============================================================================
    """
    prefix = 'noteret.tiktok.'
    for name, (tname, tname_todo, _) in PipelineInsert._REGISTRY.items():
        assert tname.startswith(prefix), (
            f'{name}: tname {tname} missing prefix')
        assert tname_todo.startswith(prefix), (
            f'{name}: tname_todo {tname_todo} missing prefix')


def test_names() -> None:
    """
    ============================================================================
     Test that names() returns sorted list of all registry keys.
    ============================================================================
    """
    names = PipelineInsert.names()
    assert names == sorted(PipelineInsert._REGISTRY.keys())


def test_run_invalid_name() -> None:
    """
    ============================================================================
     Test that run() raises ValueError on invalid name.
    ============================================================================
    """
    with pytest.raises(ValueError):
        PipelineInsert.run(name=PipelineInsert.Factory.invalid_name())
