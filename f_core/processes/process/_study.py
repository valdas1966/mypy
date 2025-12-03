from f_core.processes.process import Process


Square = Process.Factory.Square()
Square(input=2).run()

WithRecord = Process.Factory.with_record()
WithRecord().run()
