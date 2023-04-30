"""

"""

from predictor.src.stream_pipeline.agent import AgentFactory
from predictor.src.stream_pipeline.data_sink import (
    DataSinkFactory,
    AgentBasedDataSink,
    DataSink,
)
from predictor.src.stream_pipeline.pipe import PipeFactory


class AgentBasedDataSinkFactory(DataSinkFactory):
    def __init__(
        self,
        sink_topic_name: str,
        agent_factory: AgentFactory,
        sink_pipe_factory: PipeFactory,
    ):  # todo: init 승격
        self.sink_name = sink_topic_name
        self.agent_factory = agent_factory
        self.input_pipe = sink_pipe_factory.create_pipe()
        self.sink_pipe = sink_pipe_factory.create_pipe(sink_topic_name)

    def create_data_sink(self) -> DataSink:
        return AgentBasedDataSink(
            self.sink_name, self.agent_factory, self.input_pipe, self.sink_pipe
        )
