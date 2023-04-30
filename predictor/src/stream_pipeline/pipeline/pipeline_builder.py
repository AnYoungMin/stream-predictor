"""

"""
from __future__ import annotations
from predictor.src.stream_pipeline.agent import AgentFactory
from predictor.src.stream_pipeline.data_sink import DataSink
from predictor.src.stream_pipeline.data_source import DataSource, ForwardingRule
from predictor.src.stream_pipeline.pipe import Pipe
from predictor.src.stream_pipeline.pipeline import Pipeline
from predictor.src.stream_pipeline.filter import (
    PointOfTSMinmaxScalingFilter,
    TimeseriesMissingValueReplacingFilter,
    TimeSeriesPredictionFilter,
    TimeSeriesWindowingFilter,
    TimeseriesMinmaxDescalingFilter,
    Filter,
    SequentialFilterGroup,
)
from predictor.src.stream_pipeline.time_series_window import TimeSeriesWindowFactory
import torch.nn as nn
from typing import Dict, List


class PipelineBuilder:
    def __init__(self, agent_factory: AgentFactory, id: str):
        self.__agent_factory = agent_factory
        self.__id = id
        self.__minmax_scaling_filter = None
        self.__time_series_windowing_filter = None
        self.__time_series_prediction_filter = None
        self.__time_series_missing_value_replacing_filter = None
        self.__time_series_minmax_descaling_filter = None
        self.__data_source: DataSource = None
        self.__data_feeder: DataSource = None
        self.__ids_to_be_forwarded = None
        self.__data_sink: DataSink = None
        self.preprocessor: Filter = None

    def set_minmax_scaling_filter(
        self,
        filter_name: str,
        input_pipe: Pipe,
        minmax_map: Dict[str, Dict[str, float]],
    ) -> PipelineBuilder:
        self.__minmax_scaling_filter = PointOfTSMinmaxScalingFilter(
            filter_name, self.__agent_factory, input_pipe, minmax_map
        )
        return self

    def set_time_series_windowing_filter(
        self,
        filter_name: str,
        input_pipe: Pipe,
        feature_ids: List[str],
        window_factory: TimeSeriesWindowFactory,
        sliding_size: int,
    ) -> PipelineBuilder:
        self.__time_series_windowing_filter = TimeSeriesWindowingFilter(
            filter_name,
            self.__agent_factory,
            input_pipe,
            feature_ids,
            window_factory,
            sliding_size,
        )
        return self

    def set_time_series_prediction_filter(
        self,
        filter_name: str,
        input_pipe: Pipe,
        y_id: str,
        model: nn.Module,
        input_size: int,
    ) -> PipelineBuilder:
        self.__time_series_prediction_filter = TimeSeriesPredictionFilter(
            filter_name, self.__agent_factory, input_pipe, y_id, model, input_size
        )
        return self

    def set_time_series_missing_value_replacing_filter(
        self, filter_name: str, input_pipe: Pipe, replace_value_map: Dict[str, float]
    ) -> PipelineBuilder:
        self.__time_series_missing_value_replacing_filter = (
            TimeseriesMissingValueReplacingFilter(
                filter_name, self.__agent_factory, input_pipe, replace_value_map
            )
        )
        return self

    def set_time_series_minmax_descaling_filter(
        self,
        filter_name: str,
        input_pipe: Pipe,
        minmax_map: Dict[str, Dict[str, float]],
    ) -> PipelineBuilder:
        self.__time_series_minmax_descaling_filter = TimeseriesMinmaxDescalingFilter(
            filter_name, self.__agent_factory, input_pipe, minmax_map
        )
        return self

    def set_data_source_and_data_feeder(
        self,
        data_source: DataSource,
        data_feeder: DataSource,
        ids_to_be_forwarded: List[str],
    ) -> PipelineBuilder:
        self.__data_source = data_source
        self.__data_feeder = data_feeder
        self.__ids_to_be_forwarded = ids_to_be_forwarded
        return self

    def set_data_sink(self, data_sink: DataSink) -> PipelineBuilder:
        self.__data_sink = data_sink
        return self

    def build(self) -> Pipeline:
        # todo: dynamnic filter configuration
        self.preprocessor: Filter = (
            SequentialFilterGroup()
            .add(self.__minmax_scaling_filter)
            .add(self.__time_series_windowing_filter)
            .add(self.__time_series_missing_value_replacing_filter)
        )
        predictor: Filter = self.__time_series_prediction_filter
        postprocessor: Filter = SequentialFilterGroup().add(
            self.__time_series_minmax_descaling_filter
        )
        self.__apply_forwarding_rule_to_data_source_and_data_feeder()
        self.__link_data_feeder_with_preprocessor()
        self.__link_postprocessor_with_data_sink(postprocessor)
        pipeline = Pipeline(
            self.__id,
            self.__data_feeder,
            self.__data_source,
            self.preprocessor,
            predictor,
            postprocessor,
            self.__data_sink,
        )
        return pipeline

    def __apply_forwarding_rule_to_data_source_and_data_feeder(self):
        rule = ForwardingRule(
            self.__id, self.__ids_to_be_forwarded, self.preprocessor.get_input_pipe()
        )
        self.__data_source.link_pipe_with_forwarding_rule(rule)
        self.__data_feeder.link_pipe_with_forwarding_rule(rule)

    def __link_data_feeder_with_preprocessor(self):
        self.__data_feeder.add_output_pipe(self.preprocessor.get_input_pipe())

    def __link_postprocessor_with_data_sink(self, postprocessor: Filter):
        postprocessor.add_output_pipe(self.__data_sink.get_input_pipe())
