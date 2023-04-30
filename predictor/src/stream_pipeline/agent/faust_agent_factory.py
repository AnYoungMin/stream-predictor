"""

"""

from predictor.src.stream_pipeline.agent import AgentFactory, Agent, FaustAgent
from predictor.src.stream_pipeline.pipe import Pipe
from typing import Callable
import faust
import logging

logger = logging.getLogger(__name__)


class FaustAgentFactory(AgentFactory):
    def __init__(self, faust_app: faust.App):
        self.faust_app = faust_app

    def create_agent(
        self, agent_name: str, input_pipe: Pipe, process: Callable
    ) -> Agent:
        logger.info(f"create agent name: {agent_name}")
        return FaustAgent(self.faust_app, agent_name, input_pipe, process)
