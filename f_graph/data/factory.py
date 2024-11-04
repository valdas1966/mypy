from f_graph.data.i_1_one_to_one import DataOneToOne, DataABC as Data
from f_graph.data.i_1_one_to_many import DataOneToMany
from f_ds.queues.factory import Queue
from typing import Type


class FactoryData:

    @staticmethod
    def ONE_TO_ONE(type_queue: Type[Queue]) -> DataOneToOne:
        return DataOneToOne(type_queue=type_queue)

    @staticmethod
    def ONE_TO_MANY(type_queue: Type[Queue]) -> DataOneToMany:
        return DataOneToMany(type_queue=type_queue)
