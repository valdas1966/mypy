from f_core.processes.i_0_abc import ProcessABC


stam = ProcessABC(name='Stam', verbose=True)

print()

nested = ProcessABC.Factory.nested()
nested.run()
