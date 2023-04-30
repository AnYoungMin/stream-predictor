"""

"""

from dataclasses import dataclass
from predictor.src.stream_pipeline.message import TimeSeries


@dataclass
class PredictionResult:
    x: TimeSeries
    y_hat: TimeSeries
