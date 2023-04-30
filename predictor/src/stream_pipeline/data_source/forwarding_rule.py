"""

"""

from dataclasses import dataclass
from predictor.src.stream_pipeline.pipe import Pipe
from typing import List


@dataclass
class ForwardingRule:
    id: str
    ids_to_be_forwarded: List[str]
    pipe: Pipe
