from dataclasses import dataclass, field


@dataclass
class ResultTest:
    """
    ============================================================================
     Result of running pytest on a folder tree.
    ============================================================================
    """
    passed: int = 0
    failed: int = 0
    errors: int = 0
    files: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        """
        ====================================================================
         Total number of tests run.
        ====================================================================
        """
        return self.passed + self.failed + self.errors

    @property
    def is_passed(self) -> bool:
        """
        ====================================================================
         True if all tests passed (no failures or errors).
        ====================================================================
        """
        return self.failed == 0 and self.errors == 0

    def __str__(self) -> str:
        status = 'PASSED' if self.is_passed else 'FAILED'
        lines = [f'{status}: {self.passed} passed, '
                 f'{self.failed} failed, '
                 f'{self.errors} errors '
                 f'({self.files} files)']
        for name in self.failures:
            lines.append(f'  FAIL: {name}')
        return '\n'.join(lines)
