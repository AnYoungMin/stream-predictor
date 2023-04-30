import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
print(sys.path)
from aiokafka import AIOKafkaProducer
from predictor.src.stream_pipeline.agent.aiokafka_agent import EnhancedJSONEncoder
from predictor.src.stream_pipeline.time_series_window.sorted_list_based_time_series_window_factory import (
    SortedListBasedTimeSeriesWindowFactory,
)
from predictor.src.model_context.renewal_event import ContextRenewalEventHandler
from predictor.src.stream_pipeline.agent import AgentFactory, AIOKafkaAgentFactory
from predictor.src.stream_pipeline.data_sink import (
    DataSinkFactory,
    AgentBasedDataSinkFactory,
)
from predictor.src.stream_pipeline.data_source import (
    DataSourceFactory,
    LatestDataFeeder,
    AgentBasedDataSourceFactory,
)
from predictor.src.stream_pipeline.pipe import PipeFactory, AIOKafkaPipeFactory
from predictor.src.stream_pipeline.pipeline import PipelineManager
from predictor.src.stream_pipeline.time_series_window import TimeSeriesWindowFactory
from predictor.src.model_context.repository import (
    ContextCache,
    ContextRepository,
    CachedFileContextRepository,
    ContextFileSaver,
)
from predictor.src.model_context.subscriber import AsyncKafkaSubscriber
from predictor.src.loader import ContextFilesLoader, PipelinesLoader
from predictor.src.config import BrokerConfig
import asyncio
import json
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bootstrap_server = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
context_renewal_topic = os.environ.get("KAFKA_CONTEXT_RENEWAL_TOPIC")
source_topic = os.environ.get("KAFKA_SOURCE_TOPIC")
sink_topic = os.environ.get("KAFKA_SINK_TOPIC")
if bootstrap_server is None or context_renewal_topic is None or source_topic is None or sink_topic is None:
    logger.error("You must give os environ ['KAFKA_BOOTSTRAP_SERVER', 'KAFKA_CONTEXT_RENEWAL_TOPIC', 'KAFKA_SOURCE_TOPIC', 'KAFKA_SINK_TOPIC'")
    exit(1)
num_fetch_data = int(os.environ.get("APP_NUM_FETCH_DATA", "500"))
max_all_feature_arrival_timeout_milliseconds = int(
    os.environ.get("APP_MAX_ALL_FEATURE_ARRIVAL_TIMEOUT_MILLISECONDS", "2000")
)
context_dir = os.environ.get("APP_CONTEXT_DIR", "/var/cache/context")
broker_config = BrokerConfig(topics=[context_renewal_topic], brokers=[bootstrap_server])


async def main():
    loader = ContextFilesLoader(context_dir)
    contexts = loader.load_and_return_model_contexts()
    producer = AIOKafkaProducer(
        loop=asyncio.get_running_loop(),
        bootstrap_servers=[bootstrap_server],
        value_serializer=lambda v: json.dumps(v, cls=EnhancedJSONEncoder).encode(
            "utf-8"
        ),
    )
    await producer.start()
    agent_factory: AgentFactory = AIOKafkaAgentFactory([bootstrap_server], producer)
    window_factory: TimeSeriesWindowFactory = SortedListBasedTimeSeriesWindowFactory(
        max_all_feature_arrival_timeout_milliseconds
    )
    pipe_factory: PipeFactory = AIOKafkaPipeFactory()
    data_source_factory: DataSourceFactory = AgentBasedDataSourceFactory(
        agent_factory, pipe_factory
    )
    data_sink_factory: DataSinkFactory = AgentBasedDataSinkFactory(
        sink_topic, agent_factory, pipe_factory
    )

    pipeline_manager = PipelineManager(
        agent_factory,
        window_factory,
        pipe_factory,
        data_source_factory,
        source_topic,
        data_sink_factory,
    )
    pipeline_loader = PipelinesLoader(pipeline_manager)
    await pipeline_loader.load_pipelines(contexts)
    latest_data_feeder = LatestDataFeeder(
        source_topic, [bootstrap_server], num_fetch_data
    )
    for feature_id in contexts.keys():
        feeder_pipe = pipeline_manager.get_feeder_input_pipe(feature_id)
        await latest_data_feeder.feed_data_to_pipeline(feature_id, feeder_pipe)
    context_cache = ContextCache(contexts)
    saver = ContextFileSaver(context_dir)
    ctx_repository: ContextRepository = CachedFileContextRepository(
        context_cache, saver
    )
    callbacks = {
        context_renewal_topic: ContextRenewalEventHandler(
            ctx_repository, pipeline_manager, latest_data_feeder
        )
    }
    context_subscriber = AsyncKafkaSubscriber(
        broker_config=broker_config, on_message_callbacks_per_topic=callbacks
    )
    await context_subscriber.connect_broker()
    await context_subscriber.subscribe()


if __name__ == "__main__":
    asyncio.run(main())
