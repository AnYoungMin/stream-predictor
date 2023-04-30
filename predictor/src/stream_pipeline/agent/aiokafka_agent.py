"""

"""
import asyncio
import dataclasses
import json
from typing import Callable, List, Dict, Any
import pprint
from predictor.src.stream_pipeline.agent import (
    Agent,
    ConcreteDependencyMismatchException,
)
from predictor.src.stream_pipeline.pipe import Pipe, AIOKafkaPipe
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, TopicPartition
import logging

logger = logging.getLogger(__name__)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class AIOKafkaAgent(Agent):
    def __init__(
        self,
        agent_name: str,
        input_pipe: AIOKafkaPipe,
        bootstrap_servers: List[str],
        producer: AIOKafkaProducer,
        process: Callable,
    ):
        self.__check_whether_pipe_is_aiokafka_pipe_raising_exception_if_not(input_pipe)
        self.consumer = AIOKafkaConsumer(
            *input_pipe.get_topic_names(),
            loop=asyncio.get_running_loop(),
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        self.input_pipe = input_pipe
        self.agent_name = agent_name
        self.bootstrap_servers = bootstrap_servers
        self.output_pipes: List[AIOKafkaPipe] = []
        self.producer = producer
        self.process = process
        self.__agent_started = False
        self.__subscribe_task = None
        # self.__task_must_be_canceled_before_producer_stop = None

    def __check_whether_pipe_is_aiokafka_pipe_raising_exception_if_not(
        self, pipe: Pipe
    ):
        if not isinstance(pipe, AIOKafkaPipe):
            raise ConcreteDependencyMismatchException(
                "AIOKafkaAgent must use AIOKafkaPipe "
            )

    def get_input_pipe(self) -> Pipe:
        return self.input_pipe

    def add_output_pipe(self, pipe: Pipe):
        self.__check_whether_pipe_is_aiokafka_pipe_raising_exception_if_not(pipe)
        """
        if self.producer is None:
            self.__create_and_start_producer()
        """
        self.output_pipes.append(pipe)

    """
    def __create_and_start_producer(self):
        self.producer = AIOKafkaProducer(loop=asyncio.get_running_loop(), bootstrap_servers=self.bootstrap_servers, value_serializer=lambda v: json.dumps(v, cls=EnhancedJSONEncoder).encode('utf-8'))
        self.__task_must_be_canceled_before_producer_stop = asyncio.create_task(self.producer.start())
    """

    async def activate(self):
        try:
            if not self.__agent_started:
                await self.consumer.start()
                self.__agent_started = True
                self.__subscribe_task = asyncio.create_task(self.__subscribe())
        except Exception as e:
            print(e)

    async def __subscribe(self):
        try:
            logger.info(
                f"Agent {self.agent_name}'s subscription started: assigned {self.consumer.assignment()}"
            )
            async for message in self.consumer:
                logger.info(f"Agent {self.agent_name}'s data arrive:")
                pprint.pprint(message.value, width=1)
                processed_message = self.process(message.value)
                logger.info(f"Agent {self.agent_name}'s after processing:")
                pprint.pprint(processed_message, width=1)
                if processed_message is not None:
                    await self.__forward_message_to_output_pipes(processed_message)
        finally:
            logger.info(f"Agent {self.agent_name}'s subscription stop")
            await self.consumer.stop()

    async def __forward_message_to_output_pipes(self, message):
        """
        if len(self.output_pipes) > 0 and self.producer is not None:
        """
        for output_pipe in self.output_pipes:
            for topic in output_pipe.get_topic_names():
                await self.producer.send(topic, message)
        await self.producer.flush()

    async def deactivate(self):
        if self.__agent_started:
            self.__subscribe_task.cancel()
            await self.consumer.stop()
        """
        if self.producer is not None:
            #self.__task_must_be_canceled_before_producer_stop.cancel()
            await self.producer.stop()
        """

    async def send_message(
        self, message: Dict[str, Any], pipe: Pipe
    ):  # todo: using self.output_pipe with metadata
        self.__check_whether_pipe_is_aiokafka_pipe_raising_exception_if_not(pipe)
        """
        if self.producer is None:
            self.__create_and_start_producer()
        """
        await self.producer.send(pipe.get_topic_names()[0], message)
        await self.producer.flush()
