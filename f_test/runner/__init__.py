from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_test.runner.main import TestRunner

ULazy.install(globals(), {'TestRunner': 'f_test.runner.main:TestRunner'})
