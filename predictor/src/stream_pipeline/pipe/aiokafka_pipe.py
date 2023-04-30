"""

"""
from typing import List, Optional, Union

from predictor.src.stream_pipeline.pipe import Pipe


class AIOKafkaPipe(Pipe):
    def __init__(self, pipe_names: List[str]):
        self.pipe_names = pipe_names

    def get_topic_names(self) -> List[str]:
        return self.pipe_names
