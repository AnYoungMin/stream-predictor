"""

"""

from abc import ABC, abstractmethod
from typing import Callable
from predictor.src.stream_pipeline.agent import Agent
from predictor.src.stream_pipeline.pipe import Pipe


class AgentFactory(ABC):
    @abstractmethod
    def create_agent(
        self, agent_name: str, input_pipe: Pipe, process: Callable
    ) -> Agent:
        pass
