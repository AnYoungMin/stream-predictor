"""

"""

from typing import List
from dataclasses import dataclass
from predictor.src.stream_pipeline.message import UnivariateTimeSeriesVariable


@dataclass
class TimeSeries:
    variables: List[UnivariateTimeSeriesVariable]
    timestamps: List[int]  # todo: datetime?
