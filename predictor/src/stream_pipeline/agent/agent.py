"""

"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from predictor.src.stream_pipeline.pipe import Pipe

# todo: generic


class Agent(ABC):
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

    @abstractmethod
    async def send_message(self, message: Dict[str, Any], output_pipe: Pipe):
        pass
