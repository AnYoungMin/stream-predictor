"""

"""

from predictor.src.stream_pipeline.filter import LeafFilter
from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.pipe import Pipe
from predictor.src.stream_pipeline.message import PointOfTimeSeries
from typing import Dict


class PointOfTSMinmaxScalingFilter(LeafFilter):
    def __init__(
        self,
        filter_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        minmax_map: Dict[str, Dict[str, float]],
    ):
        super().__init__(filter_name, agent_factory, input_pipe, minmax_map)

    def create_agent(
        self,
        agent_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        minmax_map: Dict[str, Dict[str, float]],
    ) -> Agent:
        def scale_minmax(point) -> PointOfTimeSeries:
            id = point["feature_id"]
            if (
                minmax_map[id]["scaled"]
                and minmax_map[id]["scaling_strategy"] == "minmax"
            ):
                _min = minmax_map[id]["min"]
                _max = minmax_map[id]["max"]
                scaled_value = (point["value"] - _min) / (_max - _min)
                return PointOfTimeSeries(id, scaled_value, point["timestamp"])
            elif not minmax_map[id]["scaled"]:
                return point
            else:
                # todo: generalize strategy not only minmax
                return point

        agent = agent_factory.create_agent(agent_name, input_pipe, scale_minmax)
        return agent
