from f_abstract.inner.process.a_1_2_init_io import ProcessInitIO

"""
================================================================================
 Check: Input & Output Properties.
================================================================================
"""


class Process(ProcessInitIO):

    def _run(self) -> None:
        self._output = 'output'


p = Process(input='input')
print(p.input, p.output)
