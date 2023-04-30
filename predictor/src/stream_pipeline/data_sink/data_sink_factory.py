"""

"""

from abc import ABC, abstractmethod
from predictor.src.stream_pipeline.data_sink import DataSink


class DataSinkFactory(ABC):
    @abstractmethod
    def create_data_sink(self) -> DataSink:
        pass
