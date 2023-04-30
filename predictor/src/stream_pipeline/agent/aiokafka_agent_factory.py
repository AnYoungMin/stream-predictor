"""

"""
from aiokafka import AIOKafkaProducer

from predictor.src.stream_pipeline.agent import AgentFactory, Agent, AIOKafkaAgent
from predictor.src.stream_pipeline.pipe import Pipe
from typing import Callable, List
import logging

logger = logging.getLogger(__name__)


class AIOKafkaAgentFactory(AgentFactory):
    def __init__(self, bootstrap_servers: List[str], producer: AIOKafkaProducer):
        self.bootstrap_servers = bootstrap_servers
        self.producer = producer

    def create_agent(
        self, agent_name: str, input_pipe: Pipe, process: Callable
    ) -> Agent:
        logger.info(f"create aiokafka agent name: {agent_name}")
        return AIOKafkaAgent(
            agent_name, input_pipe, self.bootstrap_servers, self.producer, process
        )
