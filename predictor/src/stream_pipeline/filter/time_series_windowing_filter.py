"""

"""

from predictor.src.stream_pipeline.filter import LeafFilter
from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.pipe import Pipe
from predictor.src.stream_pipeline.message import TimeSeries, PointOfTimeSeries
from predictor.src.stream_pipeline.time_series_window import TimeSeriesWindowFactory
from typing import List, Optional, Dict, Any


# todo: 데이터 포맷 모음폴더로(dataclass로할지, faust.record로할지)


class TimeSeriesWindowingFilter(LeafFilter):
    def __init__(
        self,
        filter_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        feature_ids: List[str],
        window_factory: TimeSeriesWindowFactory,
        sliding_size: int,
    ):
        super().__init__(
            filter_name,
            agent_factory,
            input_pipe,
            feature_ids,
            window_factory,
            sliding_size,
        )

    def create_agent(
        self,
        agent_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        feature_ids: List[str],
        window_factory: TimeSeriesWindowFactory,
        sliding_size: int,
    ) -> Agent:
        _window = window_factory.create_time_series_window(sliding_size, feature_ids)

        def window(point_value: Dict[str, Any]) -> Optional[TimeSeries]:
            point = PointOfTimeSeries(
                point_value["feature_id"],
                point_value["value"],
                point_value["timestamp"],
            )
            ts = _window.add_point_and_return_ts_if_new_ts_is_constructed_else_none(
                point
            )
            return ts

        agent = agent_factory.create_agent(agent_name, input_pipe, window)
        return agent
