from f_ds.queues.i_1_priority.main import QueuePriority


queue = QueuePriority[str, int]()
queue.push(item='A', priority=3)
queue.push(item='B', priority=1)
queue.push(item='C', priority=2)
print(queue)
