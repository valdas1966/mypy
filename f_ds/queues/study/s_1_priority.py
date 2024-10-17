from f_ds.queues.i_1_priority import QueuePriority, Comparable


class C(Comparable):

    def __init__(self, val: int) -> None:
        self.val = val

    def key_comparison(self) -> list:
        return [self.val]

    def __str__(self) -> str:
        return str(self.val)


a = C(val=2)
b = C(val=1)

q = QueuePriority[C]()
q.push(item=a)
q.push(item=b)
b.val = 3
print(q.pop())
print(q.pop())