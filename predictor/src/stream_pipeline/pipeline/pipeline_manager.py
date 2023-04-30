"""

"""
from predictor.src.stream_pipeline.agent import AgentFactory
from predictor.src.stream_pipeline.data_sink import DataSinkFactory
from predictor.src.stream_pipeline.data_source import (
    DataSourceFactory,
    LatestDataFeeder,
)
from predictor.src.stream_pipeline.time_series_window import TimeSeriesWindowFactory
from predictor.src.utils import SingletonMeta
from predictor.src.shared.context import ModelContext
from predictor.src.model_context.renewal_event import ParsedContext, ContextParser
from predictor.src.stream_pipeline.pipeline import Pipeline, PipelineBuilder
from predictor.src.stream_pipeline.pipe import PipeFactory, Pipe
from typing import Dict


class PipelineManager(metaclass=SingletonMeta):
    def __init__(
        self,
        agent_factory: AgentFactory,
        window_factory: TimeSeriesWindowFactory,
        pipe_factory: PipeFactory,
        data_source_factory: DataSourceFactory,
        source_topic_name: str,
        data_sink_factory: DataSinkFactory,
    ):
        cls = type(self)
        if not hasattr(cls, "_init"):
            cls._init = True
            self.pipelines: Dict[str, Pipeline] = dict()
            self.agent_factory = agent_factory
            self.window_factory = window_factory
            self.pipe_factory = pipe_factory
            self.data_source = data_source_factory.create_data_source(source_topic_name)
            self.data_sink = data_sink_factory.create_data_sink()
            self.data_source_factory = data_source_factory
            self.is_started_source_and_sink = False

    async def renew_pipeline(self, context: ModelContext):
        parsed_context = ContextParser(context).parse_context()
        await self.__start_source_and_sink_when_not_started()
        if context.id in self.pipelines:
            await self.__tear_pipeline_down(context.id)
        self.pipelines[context.id] = self.__build_pipeline(parsed_context)
        print("#######before pipeline activate")
        await self.pipelines[context.id].activate()
        print("#######after pipeline activate")

    async def __start_source_and_sink_when_not_started(self):
        if not self.is_started_source_and_sink:
            await self.data_source.activate()
            await self.data_sink.activate()

    async def __tear_pipeline_down(self, feature_id: str):
        await self.pipelines[feature_id].tear_down()

    def __build_pipeline(self, parsed_ctx: ParsedContext) -> Pipeline:
        id = parsed_ctx.id
        builder = PipelineBuilder(self.agent_factory, id)
        builder.set_minmax_scaling_filter(
            self.__name_filter(id, "minmax_scaling"),
            self.pipe_factory.create_pipe(self.__name_input_pipe(id, "minmax_scaling")),
            parsed_ctx.scaling_map,
        )
        builder.set_time_series_windowing_filter(
            self.__name_filter(id, "time_series_windowing_filter"),
            self.pipe_factory.create_pipe(
                self.__name_input_pipe(id, "time_series_windowing_filter")
            ),
            parsed_ctx.ids_to_be_forwarded,
            self.window_factory,
            parsed_ctx.sliding_size,
        )
        builder.set_time_series_prediction_filter(
            self.__name_filter(id, "time_series_prediction_filter"),
            self.pipe_factory.create_pipe(
                self.__name_input_pipe(id, "time_series_prediction_filter")
            ),
            id,
            parsed_ctx.model,
            len(parsed_ctx.ids_to_be_forwarded),
        )
        builder.set_time_series_missing_value_replacing_filter(
            self.__name_filter(id, "missing_value_replacing_filter"),
            self.pipe_factory.create_pipe(
                self.__name_input_pipe(id, "missing_value_replacing_filter")
            ),
            parsed_ctx.x_replacing_value_map,
        )
        builder.set_time_series_minmax_descaling_filter(
            self.__name_filter(id, "time_series_minmax_descaling_filter"),
            self.pipe_factory.create_pipe(
                self.__name_input_pipe(id, "time_series_minmax_descaling_filter")
            ),
            parsed_ctx.scaling_map,
        )
        feeder_name = self.__create_data_feeder_name(id)
        data_feeder = self.data_source_factory.create_data_source(feeder_name)
        builder.set_data_source_and_data_feeder(
            self.data_source, data_feeder, parsed_ctx.ids_to_be_forwarded
        )
        builder.set_data_sink(self.data_sink)
        return builder.build()

    def __name_filter(self, feature_id: str, filter_type: str) -> str:
        filter_name = feature_id + "_pipeline_" + filter_type + "_filter"
        return filter_name

    def __name_input_pipe(self, feature_id: str, filter_type: str) -> str:
        pipe_name = feature_id + "_pipeline_" + filter_type + "_input_pipe"
        return pipe_name

    def __create_data_feeder_name(self, feature_id: str):
        return feature_id + "_data_feeder"

    def get_forwarding_rule_by_id(self, feature_id):
        return self.pipelines[feature_id].get_forwarding_rule()

    async def tear_pipelines_down(self):
        await self.data_source.deactivate()
        for feature_id, pipeline in self.pipelines.items():
            await pipeline.tear_down()
        await self.data_sink.deactivate()

    def get_feeder_input_pipe(self, feature_id: str) -> Pipe:
        return self.pipelines[feature_id].get_feeder_input_pipe()
