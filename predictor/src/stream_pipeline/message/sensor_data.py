"""

"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SensorData:
    data_id: int  # notice: int, but: PointOfTimeSeries.feature_id -> str
    created_at: int
    input_data: float
    ss_id: int
