"""

"""
from typing import Optional

from predictor.src.stream_pipeline.message import PointOfTimeSeries, TimeSeries
from predictor.src.stream_pipeline.time_series_window import (
    TimeSeriesWindow,
    EmptyFeatureException,
    SortedListBasedTimeSeriesCreator,
)
import threading
from typing import List, Dict


class SortedListBasedTimeSeriesWindow(TimeSeriesWindow):
    def __init__(
        self,
        feature_ids: List[str],
        sliding_size: int,
        max_all_feature_arrival_timeout_milliseconds: int,
    ):
        self.feature_ids = feature_ids
        self.sliding_size = sliding_size
        self.max_all_feature_arrival_timeout_milliseconds = (
            max_all_feature_arrival_timeout_milliseconds
        )
        self.windows: Dict[str, List[PointOfTimeSeries]] = dict()
        for feature_id in feature_ids:
            self.windows[feature_id] = []
        self._lock = threading.Lock()

    def add_point_and_return_ts_if_new_ts_is_constructed_else_none(
        self, point: PointOfTimeSeries
    ) -> Optional[TimeSeries]:
        self._lock.acquire()

        self.__add_point(point)
        if self.__is_possible_to_create_new_ts():
            ts = self.__create_time_series()
        else:
            ts = None
        self.__cut_stale_points()

        self._lock.release()
        return ts

    def __add_point(self, point: PointOfTimeSeries):
        self.windows[point.feature_id].append(point)
        self.windows[point.feature_id].sort(key=lambda _point: _point.timestamp)

    def __is_possible_to_create_new_ts(self) -> bool:
        return (
            self.__check_whether_all_features_arrive_at_current_point()
            and self.__check_whether_there_is_sufficient_features()
        )

    def __check_whether_all_features_arrive_at_current_point(self) -> bool:
        try:
            latest_points: List[
                PointOfTimeSeries
            ] = (
                self.__get_latest_points_from_each_feature_raising_exception_when_there_is_empty_one()
            )
        except EmptyFeatureException as e:
            return False
        else:
            return self.__are_points_within_max_timeout(latest_points)

    def __get_latest_points_from_each_feature_raising_exception_when_there_is_empty_one(
        self,
    ) -> List[PointOfTimeSeries]:
        latest_points = []
        for feature_id, window in self.windows.items():
            if len(window) == 0:
                raise EmptyFeatureException(
                    f"feature id {feature_id} has no points in window"
                )
            latest_points.append(window[-1])
        return latest_points

    def __are_points_within_max_timeout(
        self, latest_points: List[PointOfTimeSeries]
    ) -> bool:
        max_timestamp = max(point.timestamp for point in latest_points)
        min_timestamp = min(point.timestamp for point in latest_points)
        return (
            max_timestamp - min_timestamp
        ) <= self.max_all_feature_arrival_timeout_milliseconds

    def __check_whether_there_is_sufficient_features(self) -> bool:
        for feature_id, window in self.windows.items():
            if len(window) >= self.sliding_size:
                return True
        return False

    def __create_time_series(self) -> TimeSeries:
        ts_creator = SortedListBasedTimeSeriesCreator(
            self.feature_ids,
            self.windows,
            self.sliding_size,
            self.max_all_feature_arrival_timeout_milliseconds,
        )
        ts = ts_creator.create_time_series_from_windows()
        return ts

    def __cut_stale_points(self):
        for feature_id, window in self.windows.items():
            if len(window) > self.sliding_size:
                self.windows[feature_id] = window[len(window) - self.sliding_size :]
