"""

"""

from dataclasses import dataclass, field


@dataclass
class PointOfTimeSeries:
    feature_id: str
    value: float
    timestamp: int  # todo: datetime
