"""

"""

from dataclasses import dataclass
from typing import List


@dataclass
class BrokerConfig:
    topics: List[str]
    brokers: List[str]
