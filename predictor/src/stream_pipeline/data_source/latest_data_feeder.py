"""

"""

from predictor.src.stream_pipeline.data_source import ForwardingRule, DataSourceFactory
from kafka import KafkaConsumer, TopicPartition, KafkaProducer
from typing import List, Any
import logging

from predictor.src.stream_pipeline.pipe import Pipe

logger = logging.getLogger(__name__)


class LatestDataFeeder:
    def __init__(
        self, source_topic_name: str, bootstrap_servers: List[str], num_fetch_data: int
    ):
        self.partition = TopicPartition(source_topic_name, 0)
        self.consumer = self.__create_and_initialize_source_consumer(bootstrap_servers)
        self.num_fetch_data = num_fetch_data
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.__real_num_fetch_data = num_fetch_data

    def __create_and_initialize_source_consumer(self, bootstrap_servers: List[str]):
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
        consumer.assign([self.partition])
        return consumer

    async def feed_data_to_pipeline(self, feature_id: str, feeder_input_pipe: Pipe):
        self.__seek_offset()
        data = self.__fetch_data()
        logger.info(f"Fetched feeding data: {data}")
        await self.__feed_data_to_pipeline(
            feature_id, feeder_input_pipe, data
        )  # todo: destructor

    def __seek_offset(self):
        end_offset = self.consumer.end_offsets([self.partition])[self.partition]
        logger.info(f"data source topic's end offset: {end_offset}")
        feed_start_offset = (
            end_offset - self.num_fetch_data
            if end_offset - self.num_fetch_data > 0
            else 1
        )
        self.__real_num_fetch_data = min(self.num_fetch_data, end_offset)
        logger.info(
            f"feed start offset: {feed_start_offset}, num fetch data: {self.num_fetch_data}"
        )
        self.consumer.seek(self.partition, feed_start_offset)

    def __fetch_data(self) -> List[Any]:  # todo: type
        data = []
        for message in self.consumer:
            data.append(message.value)
            if len(data) >= self.__real_num_fetch_data:
                break
        return data

    async def __feed_data_to_pipeline(
        self, feature_id: str, feeder_input_pipe: Pipe, data: List[Any]
    ):
        for value in data:
            self.producer.send(*feeder_input_pipe.get_topic_names(), value)
        self.producer.flush()

    async def close(self):
        await self.comsumer.stop()
        await self.producer.stop()
