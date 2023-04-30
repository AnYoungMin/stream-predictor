"""

"""

from abc import ABC, abstractmethod
from predictor.src.stream_pipeline.pipe import Pipe


class Filter(ABC):
    @abstractmethod
    def get_input_pipe(self) -> Pipe:
        pass

    @abstractmethod
    def add_output_pipe(self, pipe: Pipe):
        pass

    @abstractmethod
    async def activate(self):
        pass

    @abstractmethod
    async def deactivate(self):
        pass
