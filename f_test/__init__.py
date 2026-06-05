from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_test.result.main import ResultTest
    from f_test.runner.main import TestRunner

ULazy.install(globals(), {
    'ResultTest': 'f_test.result.main:ResultTest',
    'TestRunner': 'f_test.runner.main:TestRunner',
})
