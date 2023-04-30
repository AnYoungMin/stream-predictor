"""

"""

from predictor.src.shared.context import ModelContext
from predictor.src.model_context.repository import ContextRepository
from predictor.src.stream_pipeline.data_source import LatestDataFeeder
from predictor.src.stream_pipeline.pipeline.pipeline_manager import PipelineManager
import logging

logger = logging.getLogger(__name__)


class ContextRenewalEventHandler:
    def __init__(
        self,
        context_repository: ContextRepository,
        pipeline_manager: PipelineManager,
        latest_data_feeder: LatestDataFeeder,
    ):
        self.context_repository = context_repository
        self.pipeline_manager = pipeline_manager
        self.latest_data_feeder = latest_data_feeder

    async def __call__(self, context: ModelContext):
        try:
            self.context_repository.save(context)
            await self.pipeline_manager.renew_pipeline(context)
            feeder_pipe = self.pipeline_manager.get_feeder_input_pipe(context.id)
            await self.latest_data_feeder.feed_data_to_pipeline(context.id, feeder_pipe)
        except Exception as e:
            logger.error(e)
            