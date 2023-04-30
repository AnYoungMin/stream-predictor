"""

"""

from predictor.src.stream_pipeline.filter import LeafFilter
from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.message import (
    UnivariateTimeSeriesVariable,
    TimeSeries,
)
from predictor.src.stream_pipeline.pipe import Pipe
from typing import Dict, Callable, Optional


class TimeseriesMissingValueReplacingFilter(LeafFilter):
    def __init__(
        self,
        filter_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        replace_value_map: Dict[str, float],
    ):
        super().__init__(filter_name, agent_factory, input_pipe, replace_value_map)

    def create_agent(
        self,
        agent_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        replace_value_map: Dict[str, float],
    ) -> Agent:
        def replace_missing_value(series) -> TimeSeries:
            def replace_value(
                _replace_value: float,
            ) -> Callable[[Optional[float]], float]:
                replace_func: Callable[[Optional[float]], float] = (
                    lambda value: _replace_value if value is None else value
                )
                return replace_func

            def replace_uni_series() -> (
                Callable[[UnivariateTimeSeriesVariable], UnivariateTimeSeriesVariable]
            ):
                replace_func: Callable[
                    [UnivariateTimeSeriesVariable], UnivariateTimeSeriesVariable
                ] = lambda variable: UnivariateTimeSeriesVariable(
                    id=variable["id"],
                    values=list(
                        map(
                            replace_value(replace_value_map[variable["id"]]),
                            variable["values"],
                        )
                    ),
                )
                return replace_func

            replaced_series = TimeSeries(
                variables=list(map(replace_uni_series(), series["variables"])),
                timestamps=series["timestamps"],
            )
            return replaced_series

        agent = agent_factory.create_agent(
            agent_name, input_pipe, replace_missing_value
        )
        return agent
