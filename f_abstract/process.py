from abc import ABC, abstractmethod


class Process(ABC):

    @abstractmethod
    def run(self) -> None:
        pass
