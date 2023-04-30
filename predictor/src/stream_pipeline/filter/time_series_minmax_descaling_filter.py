"""

"""

from predictor.src.stream_pipeline.filter import LeafFilter
from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.message import (
    UnivariateTimeSeriesVariable,
    TimeSeries,
)
from predictor.src.stream_pipeline.message.prediction_result import PredictionResult
from predictor.src.stream_pipeline.pipe import Pipe
from typing import Dict, Callable, List, Any


class TimeseriesMinmaxDescalingFilter(LeafFilter):
    def __init__(
        self,
        filter_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        minmax_map: Dict[str, Dict[str, float]],
    ):
        self.minmax_map = minmax_map
        super().__init__(filter_name, agent_factory, input_pipe)

    def create_agent(
        self, agent_name: str, agent_factory: AgentFactory, input_pipe: Pipe
    ) -> Agent:
        def descale_minmax(prediction_result) -> TimeSeries:
            descaled_x_variables: List[UnivariateTimeSeriesVariable] = []
            series = prediction_result["x"]
            for variable in series["variables"]:
                descaled_variable = self.__descale_variable(variable)
                descaled_x_variables.append(descaled_variable)
            descaled_x = TimeSeries(descaled_x_variables, series["timestamps"])
            descaled_y_hat_variables: List[UnivariateTimeSeriesVariable] = []
            series = prediction_result["y_hat"]
            for variable in series["variables"]:
                descaled_variable = self.__descale_variable(variable)
                descaled_y_hat_variables.append(descaled_variable)
            descaled_y_hat = TimeSeries(descaled_y_hat_variables, series["timestamps"])
            return PredictionResult(descaled_x, descaled_y_hat)

        agent = agent_factory.create_agent(agent_name, input_pipe, descale_minmax)
        return agent

    def __descale_variable(self, variable: Dict[str, Any]):
        if (
            self.minmax_map[variable["id"]]["scaled"]
            and self.minmax_map[variable["id"]]["scaling_strategy"] == "minmax"
        ):
            _min = self.minmax_map[variable["id"]]["min"]
            _max = self.minmax_map[variable["id"]]["max"]
            descaled_variable = UnivariateTimeSeriesVariable(
                variable["id"],
                list(
                    map(
                        lambda value: (value * (_max - _min)) + _min, variable["values"]
                    )
                ),
            )
        elif not self.minmax_map[variable["id"]]["scaled"]:
            descaled_variable = UnivariateTimeSeriesVariable(**variable)
        else:
            # todo: generalize strategy not only minmax
            descaled_variable = UnivariateTimeSeriesVariable(**variable)
        return descaled_variable
