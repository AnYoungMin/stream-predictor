"""

"""

from abc import ABC, abstractmethod
from predictor.src.stream_pipeline.time_series_window import TimeSeriesWindow
from typing import List


class TimeSeriesWindowFactory(ABC):
    def __init__(self, max_all_feature_arrival_timeout_milliseconds: int):
        self.max_all_feature_arrival_timeout_milliseconds = (
            max_all_feature_arrival_timeout_milliseconds
        )

    @abstractmethod
    def create_time_series_window(
        self, sliding_size: int, feature_ids: List[str]
    ) -> TimeSeriesWindow:
        pass
