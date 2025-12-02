from f_core.processes.i_2_io import ProcessIO


Square = ProcessIO.Factory.square()
Square(input=2).run()
