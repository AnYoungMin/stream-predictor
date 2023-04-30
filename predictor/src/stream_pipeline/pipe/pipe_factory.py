"""

"""

from abc import ABC, abstractmethod
from predictor.src.stream_pipeline.pipe import Pipe
from typing import Optional, List, Union


class PipeFactory(ABC):
    @abstractmethod
    def create_pipe(self, pipe_name: Optional[Union[str, List[str]]] = None) -> Pipe:
        pass
