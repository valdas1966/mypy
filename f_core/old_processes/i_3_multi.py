from f_core.processes.i_1_input import ProcessInput, Input
from f_core.old_processes import ProcessSequence, DataSequence
from concurrent.futures import ThreadPoolExecutor, Future
from f_ds.groups.group import Group
from typing import Generic, TypeVar, Type
from dataclasses import dataclass


Process = TypeVar('Process', bound=ProcessInput)

@dataclass
class DataInput(Generic[Process, Input]):
    """
    ============================================================================
     DataClass for ProcessInputMulti Input.
    ============================================================================
    """
    # Process to be executed
    process: Type[Process]
    # List of inputs to be processed
    inputs: list[Input] 
    # Number of threads to use
    threads: int


class ProcessMulti(Generic[Process], ProcessInput[DataInput]):
    """
    ============================================================================
     Process multiple Input-Processes in parallel.
    ============================================================================
    """

    def __init__(self,
                 _input: DataInput,
                 verbose: bool = True,
                 name: str = 'Multi-Process Input') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessInput.__init__(self, _input=_input, verbose=verbose, name=name)
        self._type_process: Type[Process] = _input.process
        self._inputs: list[Input] = _input.inputs
        # lower bound for number of threads
        self._threads = min(_input.threads, len(self._inputs))        

    def run(self) -> None:
        """
        ========================================================================
         Execute old_processes in parallel threads, where each thread executes its
         assigned old_processes sequentially. The old_processes are distributed across
         threads using self._pools.
        ========================================================================
        """
        # Run necessary operations before the start of the Process.
        self._run_pre()
        # Create groups of distributed inputs
        groups: list[Group[Input]] = Group.to_groups(data=self._inputs,
                                                     n=self._threads)
        # Create Sequence-Process for each Group
        self._processes: list[ProcessSequence] = list()
        for i, group in enumerate(groups):
            data = DataSequence(process=self._type_process, inputs=group)
            p = ProcessSequence(_input=data, name=f'{self._name}[{i+1}]')
            self._processes.append(p)
        # Run all old_processes in parallel
        with ThreadPoolExecutor(max_workers=self._threads) as executor:
            # Get futures tasks for all old_processes
            futures: list[Future[None]] = self._get_futures(executor=executor)
            # Wait for all futures to complete
            for future in futures:
                future.result()  # This ensures we catch any exceptions
        # Run necessary operations after the Process finishes.
        self._run_post()

    def _get_futures(self, executor: ThreadPoolExecutor) -> list[Future[None]]:
        """
        ========================================================================
         Convert the old_processes to futures.
        ========================================================================
        """
        futures: list[Future[None]] = []
        for process in self._processes:
            futures.append(executor.submit(process.run))
        return futures
