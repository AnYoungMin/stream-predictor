"""

"""

from predictor.src.stream_pipeline.time_series_window import (
    TimeSeriesWindow,
    TimeSeriesWindowFactory,
    SortedListBasedTimeSeriesWindow,
)
from typing import List


class SortedListBasedTimeSeriesWindowFactory(TimeSeriesWindowFactory):
    def create_time_series_window(
        self, sliding_size: int, feature_ids: List[str]
    ) -> TimeSeriesWindow:
        return SortedListBasedTimeSeriesWindow(
            feature_ids, sliding_size, self.max_all_feature_arrival_timeout_milliseconds
        )
