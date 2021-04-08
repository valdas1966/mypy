import time


class Timer:

    def __init__(self):
        """
        ===================================================================
         Description: Constructor (Init the Timer).
        ===================================================================
        """
        self.start = time.time()

    def elapsed(self):
        """
        ===================================================================
         Description: Return elapsed seconds from start of the Timer
                        and restart the Timer.
        ===================================================================
         Return: int
        ===================================================================
        """
        finish = time.time()
        seconds = round(finish - self.start)
        self.start = finish
        return seconds
