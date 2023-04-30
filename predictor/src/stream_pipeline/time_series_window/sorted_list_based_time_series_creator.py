"""

"""

from predictor.src.stream_pipeline.message import (
    PointOfTimeSeries,
    TimeSeries,
    UnivariateTimeSeriesVariable,
)
from typing import List, Dict


class SortedListBasedTimeSeriesCreator:
    def __init__(
        self,
        feature_ids: List[str],
        windows: Dict[str, List[PointOfTimeSeries]],
        sliding_size: int,
        max_all_feature_arrival_timeout_milliseconds: int,
    ):
        self.feature_ids = feature_ids
        self.windows = windows
        self.sliding_size = sliding_size
        self.max_all_feature_arrival_timeout_milliseconds = (
            max_all_feature_arrival_timeout_milliseconds
        )
        self.traverse_index = self.__initialize_traverse_index()

    def __initialize_traverse_index(self):
        traverse_index = dict()
        for feature_id in self.feature_ids:
            traverse_index[feature_id] = len(self.windows[feature_id]) - 1
        return traverse_index

    def create_time_series_from_windows(self) -> TimeSeries:
        series_of_points: List[List[PointOfTimeSeries]] = []
        while len(series_of_points) < self.sliding_size:
            latest_points = self.__gather_latest_points()
            latest_timestamp = max(point.timestamp for point in latest_points)
            diff_timestamps = self.__calc_diff_timestamp_with_one(
                latest_points, latest_timestamp
            )
            is_arrived = list(
                map(
                    lambda diff: diff
                    <= self.max_all_feature_arrival_timeout_milliseconds,
                    diff_timestamps,
                )
            )
            avg_arrived_timestamp = self.__calc_average_of_arrived_timestamp(
                latest_points, is_arrived
            )
            multivariate_point = self.__make_multivariate_point(
                latest_points, is_arrived, avg_arrived_timestamp
            )
            series_of_points.append(multivariate_point)
            self.__descend_traverse_index_of_arrived_features(is_arrived)
        series_of_points.reverse()
        ts = self.__convert_series_of_multivariate_points_into_time_series(
            series_of_points
        )
        return ts

    def __gather_latest_points(self) -> List[PointOfTimeSeries]:
        latest_points = []
        for feature_id in self.feature_ids:
            index = self.traverse_index[feature_id]
            if index >= 0:
                latest_points.append(self.windows[feature_id][index])
            else:
                latest_points.append(PointOfTimeSeries(feature_id, None, 0))
        return latest_points

    def __calc_diff_timestamp_with_one(
        self, latest_points: List[PointOfTimeSeries], timestamp: int
    ) -> List[int]:
        diff_timestamp = []
        for point in latest_points:
            diff_timestamp.append(timestamp - point.timestamp)
        return diff_timestamp

    def __calc_average_of_arrived_timestamp(
        self, points: List[PointOfTimeSeries], is_arrived: List[bool]
    ) -> int:
        _sum = 0
        arrival_cnt = 0
        for index, _is_arrived in enumerate(is_arrived):
            if _is_arrived:
                _sum += points[index].timestamp
                arrival_cnt += 1
        avg_timestamp = int(_sum / arrival_cnt)
        return avg_timestamp

    def __make_multivariate_point(
        self,
        latest_points: List[PointOfTimeSeries],
        is_arrived: List[bool],
        avg_timestamp: int,
    ) -> List[PointOfTimeSeries]:
        multivariate_point = []
        for index, point in enumerate(latest_points):
            multivariate_point.append(
                PointOfTimeSeries(
                    point.feature_id,
                    point.value if is_arrived[index] else None,
                    avg_timestamp,
                )
            )
        return multivariate_point

    def __descend_traverse_index_of_arrived_features(self, is_arrived: List[bool]):
        for i, feature_id in enumerate(self.feature_ids):
            if is_arrived[i]:
                self.traverse_index[feature_id] -= 1

    def __convert_series_of_multivariate_points_into_time_series(
        self, series_of_points: List[List[PointOfTimeSeries]]
    ) -> TimeSeries:
        values_of_each_variable: Dict[str, List[float]] = dict()
        timestamps = []
        for id_idx, feature_id in enumerate(self.feature_ids):
            values_of_each_variable[feature_id] = []
            for series_idx, multivariate_point in enumerate(series_of_points):
                values_of_each_variable[feature_id].append(
                    multivariate_point[id_idx].value
                )
                if id_idx == 0:
                    timestamps.append(multivariate_point[id_idx].timestamp)
        variables = []
        for id_idx, feature_id in enumerate(self.feature_ids):
            variable = UnivariateTimeSeriesVariable(
                feature_id, values_of_each_variable[feature_id]
            )
            variables.append(variable)
        ts = TimeSeries(variables, timestamps)
        return ts
