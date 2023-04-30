"""

"""
import asyncio
from predictor.src.model_context.subscriber import AsyncSubscriber, CustomJSONDecoder
from aiokafka import AIOKafkaConsumer
from typing import Callable, Dict
from predictor.src.config import BrokerConfig
import json
import logging

logger = logging.getLogger(__name__)


class AsyncKafkaSubscriber(AsyncSubscriber):
    def __init__(
        self,
        broker_config: BrokerConfig,
        on_message_callbacks_per_topic: Dict[str, Callable],
    ):
        self.consumer = None
        self.topics = broker_config.topics
        self.brokers = broker_config.brokers
        self.callbacks_per_topic = on_message_callbacks_per_topic

    async def connect_broker(self):
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            loop=asyncio.get_running_loop(),
            bootstrap_servers=self.brokers,
            value_deserializer=lambda v: json.loads(
                v.decode("utf-8"), cls=CustomJSONDecoder
            )
        )
        await self.consumer.start()

    async def subscribe(self):
        try:
            logger.info("Subscription started")
            async for message in self.consumer:
                logger.info("new message arrived")
                topic = message.topic
                await self.callbacks_per_topic[topic](
                    message.value
                )  # todo: only value or whole message
        finally:
            await self.consumer.stop()


# todo: 프로젝트 스트럭처 -> model부, data부 분리
