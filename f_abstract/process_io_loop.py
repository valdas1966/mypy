from f_abstract.process_io import ProcessIO
import time


class ProcessIOLoop(ProcessIO):

    def _init_add_atts(self) -> None:
        super()._init_add_atts()
        if not hasattr(self, '_secs_between_processes'):
            self._secs_between_processes = 0

    def _run(self) -> None:
        while True:
            super()._run()
            time.sleep(self._secs_between_processes)
