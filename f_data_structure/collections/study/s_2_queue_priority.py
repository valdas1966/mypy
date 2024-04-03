from f_data_structure.collections.i_2_queue_priority import QueuePriority


q = QueuePriority[int]()
q.push(2)
q.push(1)
q.push(3)
print(q)
print(q.pop())
