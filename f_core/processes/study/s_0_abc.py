from f_core.processes.i_0_abc import ProcessABC


process = ProcessABC(verbose=True, name='Process ABC')
print(process.time_start)
print(process.time_finish)
print(process.elapsed())
