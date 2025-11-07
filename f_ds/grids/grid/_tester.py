import importlib
import inspect
from pathlib import Path


def test_all() -> None:
    """
    ========================================================================
     Automatically discover and run all test functions from subfolder tester files.
    ========================================================================
    """
    # Get the current directory old_path
    current_dir = Path(__file__).parent
    
    # Find all subdirectories with _tester.py files
    test_count = 0
    
    for subfolder in current_dir.iterdir():
        if subfolder.is_dir() and (subfolder / "_tester.py").exists():
            # Import the tester module
            module_path = f"f_ds.grids.grid.{subfolder.name}._tester"
            try:
                module = importlib.import_module(module_path)
                
                # Get all functions that start with 'test_'
                test_functions = [
                    func for name, func in inspect.getmembers(module, inspect.isfunction)
                    if name.startswith('test_') and func.__module__ == module.__name__
                ]
                
                # Run each test function
                for test_func in test_functions:
                    print(f"Running {subfolder.name}.{test_func.__name__}()")
                    test_func()
                    test_count += 1
                    
            except ImportError as e:
                print(f"Warning: Could not import {module_path}: {e}")
    
    print(f"Successfully ran {test_count} tests!")


if __name__ == "__main__":
    test_all()
