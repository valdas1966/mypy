"""
============================================================================
Master Test Runner for f_gui.layout Module
============================================================================
This module automatically discovers and runs all test functions from the 
layout submodules (bounds and rect), providing comprehensive test coverage
for the entire layout system.
============================================================================
"""

import traceback
from typing import Callable, List, Tuple


def run_all_tests() -> None:
    """
    ========================================================================
    Discovers and runs all test functions from layout submodules.
    
    Automatically imports and executes:
    - bounds._tester: test_full, test_half, test_quarter
    - rect._tester: test_full, test_half, test_quarter
    ========================================================================
    """
    print("=" * 80)
    print("🧪 RUNNING ALL LAYOUT TESTS")
    print("=" * 80)
    
    # Test discovery and execution
    test_results = []
    
    # Bounds module tests
    test_results.extend(_run_bounds_tests())
    
    # Rect module tests  
    test_results.extend(_run_rect_tests())
    
    # Report results
    _print_test_summary(test_results)


def _run_bounds_tests() -> List[Tuple[str, bool, str]]:
    """
    ========================================================================
    Run all tests from bounds._tester module.
    ========================================================================
    """
    print("\n📐 Testing Bounds Module...")
    results = []
    
    try:
        from f_gui.layout.bounds._tester import (
            test_full as bounds_test_full,
            test_half as bounds_test_half, 
            test_quarter as bounds_test_quarter
        )
        
        # Define test cases
        bounds_tests = [
            ("bounds.test_full", bounds_test_full),
            ("bounds.test_half", bounds_test_half),
            ("bounds.test_quarter", bounds_test_quarter),
        ]
        
        # Execute each test
        for test_name, test_func in bounds_tests:
            success, error_msg = _execute_test(test_func)
            results.append((test_name, success, error_msg))
            _print_test_result(test_name, success, error_msg)
            
    except ImportError as e:
        error_msg = f"Failed to import bounds tests: {e}"
        results.append(("bounds.*", False, error_msg))
        print(f"❌ {error_msg}")
    
    return results


def _run_rect_tests() -> List[Tuple[str, bool, str]]:
    """
    ========================================================================
    Run all tests from rect._tester module.
    ========================================================================
    """
    print("\n📏 Testing Rect Module...")
    results = []
    
    try:
        from f_gui.layout.rect._tester import (
            test_full as rect_test_full,
            test_half as rect_test_half,
            test_quarter as rect_test_quarter
        )
        
        # Define test cases
        rect_tests = [
            ("rect.test_full", rect_test_full),
            ("rect.test_half", rect_test_half),
            ("rect.test_quarter", rect_test_quarter),
        ]
        
        # Execute each test
        for test_name, test_func in rect_tests:
            success, error_msg = _execute_test(test_func)
            results.append((test_name, success, error_msg))
            _print_test_result(test_name, success, error_msg)
            
    except ImportError as e:
        error_msg = f"Failed to import rect tests: {e}"
        results.append(("rect.*", False, error_msg))
        print(f"❌ {error_msg}")
    
    return results


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


def run_bounds_tests_only() -> None:
    """
    ========================================================================
    Run only the bounds module tests.
    ========================================================================
    """
    print("🧪 Running Bounds Tests Only...")
    results = _run_bounds_tests()
    _print_test_summary(results)


def run_rect_tests_only() -> None:
    """
    ========================================================================
    Run only the rect module tests.  
    ========================================================================
    """
    print("🧪 Running Rect Tests Only...")
    results = _run_rect_tests()
    _print_test_summary(results)


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


if __name__ == "__main__":
    """
    ========================================================================
    When run directly, execute all tests.
    ========================================================================
    """
    run_all_tests()
    print()
    test_layout_integration()