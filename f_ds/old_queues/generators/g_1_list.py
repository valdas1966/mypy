from f_ds.old_queues.i_1_list import QueueList


class GenQueueList:
    """
    ========================================================================
     Generator for QueueList.
    ========================================================================
    """

    @staticmethod
    def empty() -> QueueList[int]:
        """
        ========================================================================
         Generate an empty Queue.
        ========================================================================
        """
        return QueueList[int](name='Empty')
    
    @staticmethod
    def trio() -> QueueList[int]:
        """
        ========================================================================
         Generate a Queue with the Elements 1, 2 and 3.
        ========================================================================
        """
        q = QueueList[int](name='Trio')
        q.push(1)
        q.push(2)
        q.push(3)
        return q

