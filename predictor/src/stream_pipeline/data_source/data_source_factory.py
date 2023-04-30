"""

"""

from abc import ABC, abstractmethod
from predictor.src.stream_pipeline.data_source import DataSource


class DataSourceFactory(ABC):
    @abstractmethod
    def create_data_source(self, source_topic_name) -> DataSource:
        pass
