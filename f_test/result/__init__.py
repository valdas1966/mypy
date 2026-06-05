from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_test.result.main import ResultTest

ULazy.install(globals(), {'ResultTest': 'f_test.result.main:ResultTest'})
