"""

"""

from typing import List
from dataclasses import dataclass


@dataclass
class UnivariateTimeSeriesVariable:
    id: str
    values: List[float]  # todo: must len >= 2
