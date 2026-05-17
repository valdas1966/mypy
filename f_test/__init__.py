from f_core.imports import ULazy

ULazy.install(globals(), {
    'ResultTest': 'f_test.result.main:ResultTest',
    'TestRunner': 'f_test.runner.main:TestRunner',
})
