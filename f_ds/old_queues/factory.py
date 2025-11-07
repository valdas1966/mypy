from f_ds.old_queues.i_1_fifo import QueueFIFO, QueueBase as Queue
from f_ds.old_queues.i_1_priority import QueuePriority


class FactoryQueue:

    @staticmethod
    def FIFO() -> QueueFIFO:
        return QueueFIFO()

    @staticmethod
    def PRIORITY() -> QueuePriority:
        return QueuePriority()
