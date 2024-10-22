from f_ds.queues.i_1_fifo import QueueFIFO


fifo = QueueFIFO()
fifo.push(2)
fifo.push(1)

print(fifo)