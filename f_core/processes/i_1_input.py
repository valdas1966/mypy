from f_core.processes.i_0_abc import ProcessABC
from typing import Generic, TypeVar, Callable, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from math import ceil

Input = TypeVar('Input')
T = TypeVar('T')
R = TypeVar('R')


class ProcessInput(Generic[Input], ProcessABC):
    """
    ============================================================================
     ABC for Processes with Input.
    ============================================================================
    """

    def __init__(self,
                 _input: Input,
                 name: str = 'Process Input') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessABC.__init__(self, name=name)
        self._input = _input

    @property
    def input(self) -> Input:
        """
        ========================================================================
         Return the Input of the Process.
        ========================================================================
        """
        return self._input


def get_chunk_slice(total_items: int, chunk_size: int, chunk_index: int) -> tuple[int, int]:
    """
    ============================================================================
     Get start and end indices for a chunk given total items and chunk size.
     
     Args:
        total_items: Total number of items to be chunked
        chunk_size: Size of each chunk
        chunk_index: Index of the current chunk
     
     Returns:
        Tuple of (start_index, end_index)
    ============================================================================
    """
    start_idx = chunk_index * chunk_size
    end_idx = min(start_idx + chunk_size, total_items)
    return start_idx, end_idx


class ProcessInputMulti(Generic[T]):
    """
    ============================================================================
     Process multiple inputs using multithreading with a given Callable.
    ============================================================================
    """

    def __init__(self,
                 func: Callable[[Dict[str, Any]], None],
                 args_list: List[Dict[str, Any]],
                 num_threads: int,
                 name: str = 'Process Input Multi') -> None:
        """
        ========================================================================
         Initialize ProcessInputMulti with a callable function and its parameters.
        
         Args:
            func: Callable function to be executed (should accept Dict[str, Any])
            args_list: List of argument dictionaries to be processed
            num_threads: Number of threads to use
            name: Name of the process
        ========================================================================
        """
        self._func = func
        self._args_list = args_list
        self._num_threads = min(num_threads, len(args_list))
        self._name = name
        self._processes: List[ProcessInput[List[Dict[str, Any]]]] = []
        self._chunk_size = ceil(len(args_list) / self._num_threads)

    def _create_processes(self) -> None:
        """
        ========================================================================
         Create ProcessInput instances based on the number of threads.
        ========================================================================
        """
        for i in range(self._num_threads):
            start_idx, end_idx = get_chunk_slice(
                total_items=len(self._args_list),
                chunk_size=self._chunk_size,
                chunk_index=i
            )
            chunk_args = self._args_list[start_idx:end_idx]
            
            if chunk_args:  # Only create process if there are arguments to process
                process = ProcessInput[List[Dict[str, Any]]](
                    _input=chunk_args,
                    name=f"{self._name}_Thread_{i+1}"
                )
                self._processes.append(process)

    def run(self) -> None:
        """
        ========================================================================
         Execute all processes using ThreadPoolExecutor.
        ========================================================================
        """
        self._create_processes()
        
        with ThreadPoolExecutor(max_workers=self._num_threads) as executor:
            futures = []
            for process in self._processes:
                for arg in process.input:
                    futures.append(executor.submit(self._func, arg))
            
            # Wait for all futures to complete
            for future in futures:
                future.result()  # This ensures we catch any exceptions



