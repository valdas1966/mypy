import heapq


class OpenClosed:

    def __init__(self) -> None:
        self._open = list()
        self._closed = set()

    @property
    def open(self) -> list:
        return self._open

    @property
    def closed(self) -> list:
        return self._closed

    def push_to_open(self, item) -> None:
        heapq.heappush(self.open, item)

    def pop_from_open(self):
        return heapq.heappop()
