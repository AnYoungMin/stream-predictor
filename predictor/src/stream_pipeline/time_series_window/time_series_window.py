"""

"""

from abc import ABC, abstractmethod
from typing import Optional
from predictor.src.stream_pipeline.message import PointOfTimeSeries, TimeSeries


class TimeSeriesWindow(ABC):
    @abstractmethod
    def add_point_and_return_ts_if_new_ts_is_constructed_else_none(
        self, point: PointOfTimeSeries
    ) -> Optional[TimeSeries]:
        pass
