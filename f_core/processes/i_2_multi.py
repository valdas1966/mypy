from f_core.processes.i_1_input import ProcessInput, Input
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
                 name: str = 'Multi-Process Input') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessInput.__init__(self, _input=_input, name=name)
        self._type_process: Type[Process] = _input.process
        self._inputs: list[Input] = _input.inputs
        # lower bound for number of threads
        self._threads = min(_input.threads, len(self._inputs))
        processes = [_input.process(_input=_input,
                                    name=f'{self._name}[]) for input_item in self._inputs]
        self._pools: list[Group[Process]] = Group.to_groups(data=self._inputs,
                                                            n=self._threads,
                                                            name=self._name)
        print(type(self._pools[0][0]))

    def run(self) -> None:
        """
        ========================================================================
         Execute processes in parallel threads, where each thread executes its
         assigned processes sequentially. The processes are distributed across
         threads using self._pools.
        ========================================================================
        """
        # Run necessary operations before the start of the Process.
        self._run_pre()
        # Run all processes in parallel      
        with ThreadPoolExecutor(max_workers=self._threads) as executor:
            # Get futures tasks for all processes
            futures: list[Future[None]] = self._get_futures(executor=executor)
            
            # Wait for all futures to complete
            for future in futures:
                future.result()  # This ensures we catch any exceptions
        # Run necessary operations after the Process finishes.
        self._run_post()

    def run_group(self, group: Group[Process]) -> None:
        """
        ========================================================================
         Run all processes in a group sequentially.
        ========================================================================
        """
        for process in group:
            process.run()

    def _get_futures(self, executor: ThreadPoolExecutor) -> list[Future[None]]:
        """
        ========================================================================
         Convert the processes to futures.
        ========================================================================
        """
        futures: list[Future[None]] = []
        for group in self._pools:
            futures.append(executor.submit(self.run_group, group))
        return futures
