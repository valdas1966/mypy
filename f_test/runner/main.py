import inspect
import os
import sys
import pytest
from pathlib import Path
from f_test.result import ResultTest


_GREEN = '\033[32m'
_RED = '\033[31m'
_BOLD = '\033[1m'
_RESET = '\033[0m'
_CYAN = '\033[36m'
_W = 80


class _ResultCollector:
    """
    ============================================================================
     Pytest plugin that collects test results grouped by module.
    ============================================================================
    """

    def __init__(self, path_root: str) -> None:
        self.result = ResultTest()
        self._path_root = Path(path_root)
        # {relative_path: [(test_name, status, error_msg)]}
        self._modules: dict[str, list[tuple[str, str, str]]] = {}

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        """
        ====================================================================
         Called for each test phase (setup, call, teardown).
        ====================================================================
        """
        if report.when != 'call':
            return
        # Parse nodeid: "path/file.py::TestClass::test_method"
        parts = report.nodeid.split('::')
        file_path = parts[0]
        test_name = '::'.join(parts[1:])
        try:
            rel = str(Path(file_path).relative_to(self._path_root))
        except ValueError:
            rel = file_path
        if rel not in self._modules:
            self._modules[rel] = []
        if report.passed:
            self.result.passed += 1
            self._modules[rel].append((test_name, 'passed', ''))
        elif report.failed:
            self.result.failed += 1
            self.result.failures.append(report.nodeid)
            error = ''
            if report.longreprtext:
                lines = report.longreprtext.strip().split('\n')
                error = lines[-1].strip() if lines else ''
            self._modules[rel].append((test_name, 'failed', error))

    def pytest_internalerror(self,
                             excrepr: object,
                             excinfo: object) -> None:
        """
        ====================================================================
         Called on internal pytest errors.
        ====================================================================
        """
        self.result.errors += 1

    def print_report(self) -> None:
        """
        ====================================================================
         Print formatted test report with colors.
        ====================================================================
        """
        for module, tests in self._modules.items():
            print()
            print(f'{_CYAN}{"═" * _W}{_RESET}')
            print(f' {_BOLD}{module}{_RESET}')
            print(f'{_CYAN}{"─" * _W}{_RESET}')
            for test_name, status, error in tests:
                if status == 'passed':
                    print(f'  {_GREEN}✓ {test_name}{_RESET}')
                else:
                    print(f'  {_RED}✗ {test_name}{_RESET}')
                    if error:
                        print(f'    {_RED}{error}{_RESET}')
        # Summary
        print()
        r = self.result
        c = f'{_GREEN}{_BOLD}' if r.is_passed else f'{_RED}{_BOLD}'
        tag = 'PASSED' if r.is_passed else 'FAILED'
        print(f'{c}{"═" * _W}{_RESET}')
        print(f'{c} {tag}: {r.passed} passed, {r.failed} failed, '
              f'{r.errors} errors ({r.files} files){_RESET}')
        print(f'{c}{"═" * _W}{_RESET}')


class TestRunner:
    """
    ============================================================================
     Run all _tester.py pytest files in a folder and its sub-folders.
    ============================================================================
    """

    @staticmethod
    def run(path_folder: str = None,
            pattern: str = '_tester*.py',
            verbose: bool = False) -> ResultTest:
        """
        ====================================================================
         Run all pytest files matching pattern in the folder tree.
         If path_folder is None, auto-detects the caller's directory.
         Default pattern '_tester*.py' picks up both the base
         '_tester.py' file and any concern-split siblings like
         '_tester_grid.py' or '_tester_recording.py'.
        ====================================================================
        """
        if path_folder is None:
            caller_file = inspect.stack()[1].filename
            path_folder = str(Path(caller_file).parent)
        folder = Path(path_folder)
        files = sorted(str(p) for p in folder.rglob(pattern))
        collector = _ResultCollector(path_root=path_folder)
        collector.result.files = len(files)
        if not files:
            collector.print_report()
            return collector.result
        args = files + ['--tb=no', '-q', '--no-header']
        # Suppress pytest terminal output
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            pytest.main(args=args, plugins=[collector])
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout
        collector.print_report()
        return collector.result
