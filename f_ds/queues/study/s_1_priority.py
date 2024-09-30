from f_ds.queues.i_1_priority import QueuePriority


q = QueuePriority[int]()
q.push(2)
q.push(1)
q.to_list().display()