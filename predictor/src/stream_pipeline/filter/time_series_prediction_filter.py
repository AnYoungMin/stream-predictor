"""

"""

from predictor.src.stream_pipeline.filter import LeafFilter
from predictor.src.stream_pipeline.agent import AgentFactory, Agent
from predictor.src.stream_pipeline.message.prediction_result import PredictionResult
from predictor.src.stream_pipeline.pipe import Pipe
from predictor.src.stream_pipeline.message import (
    TimeSeries,
    UnivariateTimeSeriesVariable,
)
import torch.nn as nn
import torch
from typing import List, Callable

# todo: 데이터 포맷 모음폴더로(dataclass로할지, faust.record로할지)


class TimeSeriesPredictionFilter(LeafFilter):
    """
    Filter for predicting timeseries from timeseries window.

    Note: It is tightly coupled with PyTorch (CPU-only mode).
          It assume that input(x: TimeSeries) has accurate sequence length for model.
    """

    def __init__(
        self,
        filter_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        y_id: str,
        model: nn.Module,
        input_size: int,
    ):
        super().__init__(
            filter_name, agent_factory, input_pipe, y_id, model, input_size
        )

    def create_agent(
        self,
        agent_name: str,
        agent_factory: AgentFactory,
        input_pipe: Pipe,
        y_id: str,
        model: nn.Module,
        input_size: int,
    ) -> Agent:
        def predict(x: TimeSeries) -> TimeSeries:
            tensor_x = TimeSeriesPredictionFilter.__convert_ts_values_to_tensor(
                x, input_size
            )
            tensor_y_hat = model(tensor_x)
            list_y_hat = tensor_y_hat.reshape(-1).tolist()  # todo: if uni -> reshape
            num_step = len(list_y_hat)
            y_timestamps = TimeSeriesPredictionFilter.__predict_timestamps(
                x["timestamps"], num_step
            )
            y_hat = TimeSeriesPredictionFilter.__create_ts(
                [list_y_hat], [y_id], y_timestamps
            )
            prediction_result = PredictionResult(TimeSeries(**x), y_hat)
            return prediction_result

        agent = agent_factory.create_agent(agent_name, input_pipe, predict)
        return agent

    @staticmethod
    def __convert_ts_values_to_tensor(x, input_size: int) -> torch.Tensor:
        extract_values_func: Callable[
            [UnivariateTimeSeriesVariable], List[float]
        ] = lambda x_n: x_n["values"]
        list_x = [list(map(extract_values_func, x["variables"]))]
        tensor_x = torch.FloatTensor(list_x)  # (batch_size=1, input_size, seq_len)
        tensor_x = tensor_x.transpose(1, 2)  # (batch_size=1, seq_len, input_size)
        return tensor_x

    @staticmethod
    def __predict_timestamps(x_timestamps: List[int], num_step: int) -> List[int]:
        gaps = [
            x_timestamps[i + 1] - x_timestamps[i] for i in range(len(x_timestamps) - 1)
        ]
        most_frequent_gap = max(gaps, key=gaps.count)
        last_x_timestamp = x_timestamps[-1]
        predicted_timestamps = TimeSeriesPredictionFilter.__span_n_timestamps(
            last_x_timestamp, num_step, most_frequent_gap
        )
        return predicted_timestamps

    @staticmethod
    def __span_n_timestamps(base_timestamp: int, num_step: int, gap: int) -> List[int]:
        spanned_timestamps = [
            base_timestamp + (i * gap) for i in range(1, num_step + 1)
        ]
        return spanned_timestamps

    @staticmethod
    def __create_ts(
        values: List[List[float]], feature_ids: List[str], timestamps: List[int]
    ) -> TimeSeries:
        variables = []
        for idx, feature_id in enumerate(feature_ids):
            univariate = UnivariateTimeSeriesVariable(feature_id, values[idx])
            variables.append(univariate)
        ts = TimeSeries(variables, timestamps)
        return ts
