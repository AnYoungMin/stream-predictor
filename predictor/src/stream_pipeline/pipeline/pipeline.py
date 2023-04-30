"""

"""
from predictor.src.stream_pipeline.data_sink import DataSink
from predictor.src.stream_pipeline.data_source import DataSource, ForwardingRule
from predictor.src.stream_pipeline.filter import SequentialFilterGroup, Filter
from predictor.src.stream_pipeline.pipe import Pipe


class Pipeline:
    def __init__(
        self,
        id: str,
        data_feeder: DataSource,
        data_source: DataSource,
        preprocessor: Filter,
        predictor: Filter,
        postprocessor: Filter,
        data_sink: DataSink,
    ):
        self.id = id
        self.pipeline = (
            SequentialFilterGroup().add(preprocessor).add(predictor).add(postprocessor)
        )
        self.data_source = data_source  # todo: data_source변수 공유되는데 이거 맞나..?
        self.data_sink = data_sink
        self.data_feeder = data_feeder

    async def tear_down(self):
        self.data_source.remove_rule_by_id(self.id)
        await self.data_feeder.deactivate()
        await self.pipeline.deactivate()

    async def activate(self):
        await self.pipeline.activate()
        await self.data_feeder.activate()

    def get_forwarding_rule(self) -> ForwardingRule:
        return self.data_source.get_forwarding_rule_by_id(self.id)

    def get_feeder_input_pipe(self) -> Pipe:
        return self.data_feeder.get_input_pipe()
