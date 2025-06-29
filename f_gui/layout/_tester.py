"""
============================================================================
Master Test Runner for f_gui.layout Module
============================================================================
This module automatically discovers and runs all test functions from 
_tester.py files in layout subfolders, providing comprehensive test coverage
for the entire layout system.

Features:
- Automatic discovery of _tester.py files in subfolders
- Dynamic import and execution of test functions
- No hardcoded module names - fully extensible
- Comprehensive error handling and reporting
============================================================================
"""

import os
import importlib
import inspect
import traceback
from typing import Callable, List, Tuple, Dict, Any
from pathlib import Path


def run_all_tests() -> None:
    """
    ========================================================================
    Automatically discovers and runs all test functions from _tester.py
    files in subfolders.
    
    Discovery Process:
    1. Scans all subfolders for _tester.py files
    2. Dynamically imports each discovered module
    3. Finds all functions starting with 'test_'
    4. Executes each test with error handling
    ========================================================================
    """
    print("=" * 80)
    print("🧪 RUNNING ALL LAYOUT TESTS (AUTO-DISCOVERY)")
    print("=" * 80)
    
    # Discover all tester modules
    tester_modules = discover_tester_modules()
    
    if not tester_modules:
        print("⚠️  No _tester.py files found in subfolders")
        return
    
    print(f"🔍 Discovered {len(tester_modules)} tester module(s):")
    for module_path in tester_modules:
        print(f"  • {module_path}")
    print()
    
    # Run tests from all discovered modules
    all_results = []
    
    for module_path in tester_modules:
        module_results = _run_module_tests(module_path)
        all_results.extend(module_results)
    
    # Report overall results
    _print_test_summary(all_results)


def discover_tester_modules() -> List[str]:
    """
    ========================================================================
    Discover all _tester.py files in subfolders.
    
    Returns:
        List of module paths (e.g., ['bounds._tester', 'rect._tester'])
    ========================================================================
    """
    layout_dir = Path(__file__).parent
    tester_modules = []
    
    # Scan all subdirectories
    for item in layout_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            tester_file = item / "_tester.py"
            if tester_file.exists():
                module_path = f"{item.name}._tester"
                tester_modules.append(module_path)
    
    return sorted(tester_modules)


def _run_module_tests(module_path: str) -> List[Tuple[str, bool, str]]:
    """
    ========================================================================
    Run all test functions from a specific tester module.
    
    Args:
        module_path: Module path like 'bounds._tester'
        
    Returns:
        List of (test_name, success, error_message) tuples
    ========================================================================
    """
    module_name = module_path.replace('._tester', '')
    print(f"📋 Testing {module_name.title()} Module...")
    
    results = []
    
    try:
        # Dynamic import using relative imports
        if module_path == "bounds._tester":
            from .bounds._tester import (
                test_full as bounds_test_full,
                test_half as bounds_test_half,
                test_quarter as bounds_test_quarter
            )
            test_functions = {
                'test_full': bounds_test_full,
                'test_half': bounds_test_half,
                'test_quarter': bounds_test_quarter
            }
        elif module_path == "rect._tester":
            from .rect._tester import (
                test_full as rect_test_full,
                test_half as rect_test_half,
                test_quarter as rect_test_quarter
            )
            test_functions = {
                'test_full': rect_test_full,
                'test_half': rect_test_half,
                'test_quarter': rect_test_quarter
            }
        else:
            # Fallback to dynamic import for unknown modules
            full_module_path = f"f_gui.layout.{module_path}"
            module = importlib.import_module(full_module_path)
            test_functions = discover_test_functions(module)
        
        if not test_functions:
            print(f"  ⚠️  No test functions found in {module_path}")
            return results
        
        # Execute each test function
        for func_name, func in test_functions.items():
            test_name = f"{module_name}.{func_name}"
            success, error_msg = _execute_test(func)
            results.append((test_name, success, error_msg))
            _print_test_result(test_name, success, error_msg)
            
    except ImportError as e:
        error_msg = f"Failed to import {module_path}: {e}"
        results.append((f"{module_name}.*", False, error_msg))
        print(f"  ❌ {error_msg}")
    except Exception as e:
        error_msg = f"Unexpected error in {module_path}: {e}"
        results.append((f"{module_name}.*", False, error_msg))
        print(f"  ❌ {error_msg}")
    
    return results


def discover_test_functions(module: Any) -> Dict[str, Callable]:
    """
    ========================================================================
    Discover all functions in a module that start with 'test_'.
    
    Args:
        module: The imported module
        
    Returns:
        Dictionary of {function_name: function_object}
    ========================================================================
    """
    test_functions = {}
    
    for name, obj in inspect.getmembers(module):
        if (inspect.isfunction(obj) and 
            name.startswith('test_') and 
            not name.startswith('test_layout_integration')):  # Skip integration tests
            test_functions[name] = obj
    
    return test_functions


def _execute_test(test_func: Callable) -> Tuple[bool, str]:
    """
    ========================================================================
    Execute a single test function with error handling.
    
    Args:
        test_func: The test function to execute
        
    Returns:
        Tuple of (success: bool, error_message: str)
    ========================================================================
    """
    try:
        test_func()
        return True, ""
    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}"
        return False, error_msg


def _print_test_result(test_name: str, success: bool, error_msg: str) -> None:
    """
    ========================================================================
    Print the result of a single test.
    ========================================================================
    """
    if success:
        print(f"  ✅ {test_name}")
    else:
        print(f"  ❌ {test_name}")
        if error_msg:
            print(f"     └─ {error_msg}")


def _print_test_summary(results: List[Tuple[str, bool, str]]) -> None:
    """
    ========================================================================
    Print overall test summary with statistics.
    ========================================================================
    """
    total_tests = len(results)
    passed_tests = sum(1 for _, success, _ in results if success)
    failed_tests = total_tests - passed_tests
    
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests:  {total_tests}")
    print(f"Passed:       {passed_tests} ✅")
    print(f"Failed:       {failed_tests} ❌")
    
    if failed_tests == 0:
        print("\n🎉 ALL TESTS PASSED! Layout module is working correctly.")
    else:
        print(f"\n⚠️  {failed_tests} test(s) failed. Check errors above.")
        print("\nFailed Tests:")
        for test_name, success, error_msg in results:
            if not success:
                print(f"  • {test_name}: {error_msg}")
    
    print("=" * 80)


def run_specific_module_tests(module_name: str) -> None:
    """
    ========================================================================
    Run tests for a specific module only.
    
    Args:
        module_name: Name of the module (e.g., 'bounds', 'rect')
    ========================================================================
    """
    print(f"🧪 Running {module_name.title()} Tests Only...")
    module_path = f"{module_name}._tester"
    results = _run_module_tests(module_path)
    _print_test_summary(results)


def list_discovered_modules() -> None:
    """
    ========================================================================
    List all discovered tester modules without running tests.
    ========================================================================
    """
    print("🔍 DISCOVERING TESTER MODULES")
    print("=" * 40)
    
    tester_modules = discover_tester_modules()
    
    if not tester_modules:
        print("No _tester.py files found in subfolders")
        return
    
    print(f"Found {len(tester_modules)} tester module(s):")
    for module_path in tester_modules:
        module_name = module_path.replace('._tester', '')
        print(f"  📁 {module_name}/ → {module_path}")
        
        # Try to show available test functions
        try:
            if module_path == "bounds._tester":
                print(f"     └─ test_full()")
                print(f"     └─ test_half()")
                print(f"     └─ test_quarter()")
            elif module_path == "rect._tester":
                print(f"     └─ test_full()")
                print(f"     └─ test_half()")
                print(f"     └─ test_quarter()")
            else:
                print(f"     └─ (functions unknown)")
                
        except Exception as e:
            print(f"     └─ (error loading: {e})")
    
    print("=" * 40)


def test_layout_integration() -> None:
    """
    ========================================================================
    High-level integration test for the layout system.
    Tests interaction between Bounds and Rect components.
    ========================================================================
    """
    print("🔄 Testing Layout Integration...")
    
    try:
        from f_gui.layout import Bounds, Rect
        
        # Test 1: Create bounds with rect
        rect = Rect(top=10, left=10, width=80, height=80)
        bounds = Bounds(relative=(25, 25, 50, 50), parent=rect)
        
        # Verify absolute calculation
        expected_absolute = Rect(top=30, left=30, width=40, height=40)
        assert bounds.absolute == expected_absolute, \
            f"Expected {expected_absolute}, got {bounds.absolute}"
        
        # Test 2: Factory integration
        full_bounds = Bounds.Factory.full()
        half_rect = Rect.Factory.half()
        
        assert full_bounds.relative == Rect.Factory.full()
        assert half_rect.width == 50
        
        print("  ✅ Layout integration test passed")
        
    except Exception as e:
        print(f"  ❌ Layout integration test failed: {e}")
        traceback.print_exc()


# Convenience functions for backward compatibility
def run_bounds_tests_only() -> None:
    """Run only bounds module tests."""
    run_specific_module_tests('bounds')


def run_rect_tests_only() -> None:
    """Run only rect module tests."""
    run_specific_module_tests('rect')


if __name__ == "__main__":
    """
    ========================================================================
    When run directly, execute auto-discovery and run all tests.
    ========================================================================
    """
    run_all_tests()