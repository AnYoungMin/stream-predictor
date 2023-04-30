"""

"""

from predictor.src.stream_pipeline.agent import AgentFactory
from predictor.src.stream_pipeline.data_source import DataSource, FaustAgentDataSource
from predictor.src.stream_pipeline.data_source.data_source_factory import (
    DataSourceFactory,
)
from predictor.src.stream_pipeline.pipe import PipeFactory


class FaustAgentDataSourceFactory(DataSourceFactory):
    def __init__(self, agent_factory: AgentFactory, source_pipe_factory: PipeFactory):
        self.agent_factory = agent_factory
        self.source_pipe_factory = (
            source_pipe_factory  # todo: factory 넘겨주는지 생성해서 넘기는지 나중에 일괄되게
        )

    def create_data_source(self, source_topic_name) -> DataSource:
        source_pipe = self.source_pipe_factory.create_pipe(source_topic_name)
        return FaustAgentDataSource(source_topic_name, self.agent_factory, source_pipe)
